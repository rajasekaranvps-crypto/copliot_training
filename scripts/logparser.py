import argparse
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone

JSON_SUBSTRING = re.compile(r"\{.*\}")


def parse_json_line(line):
    line = line.strip()
    if not line:
        return None

    try:
        return json.loads(line)
    except json.JSONDecodeError:
        match = JSON_SUBSTRING.search(line)
        if not match:
            return None
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            return None

    return None


def get_field(record, names):
    for name in names:
        value = record.get(name)
        if value is not None:
            return value
    return None


def normalize_path(record):
    path = get_field(record, ["path", "endpoint", "request_path", "request_uri", "uri", "url"])
    method = get_field(record, ["method", "http_method"])
    if path is None and isinstance(record.get("request"), dict):
        path = get_field(record["request"], ["path", "uri", "url"])
        method = method or get_field(record["request"], ["method", "http_method"])

    if path is None:
        return None

    if method:
        return f"{method.upper()} {path}"
    return path


def parse_timestamp(record):
    timestamp = get_field(record, ["timestamp", "time", "date"])
    if timestamp is None:
        return None

    if isinstance(timestamp, (int, float)):
        try:
            return datetime.fromtimestamp(timestamp, tz=timezone.utc)
        except (OSError, ValueError):
            return None

    if isinstance(timestamp, str):
        ts = timestamp.strip()
        if ts.endswith("Z"):
            ts = ts[:-1] + "+00:00"
        try:
            parsed = datetime.fromisoformat(ts)
            if parsed.tzinfo is None:
                return parsed.replace(tzinfo=timezone.utc)
            return parsed.astimezone(timezone.utc)
        except ValueError:
            for fmt in ["%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%d %H:%M:%S,%f"]:
                try:
                    parsed = datetime.strptime(ts, fmt)
                    return parsed.replace(tzinfo=timezone.utc)
                except ValueError:
                    continue
    return None


def parse_duration(record):
    duration = get_field(record, ["duration", "latency", "response_time", "response_time_ms", "request_time", "elapsed"])
    if duration is None:
        return None

    try:
        value = float(duration)
    except (TypeError, ValueError):
        return None

    if "ms" in str(duration) or "_ms" in str(duration) or "response_time_ms" in record:
        return value / 1000.0
    if value > 10:
        return value / 1000.0
    return value


def parse_status(record):
    status = get_field(record, ["status", "status_code", "response_status", "http_status"])
    if status is None:
        if isinstance(record.get("response"), dict):
            status = get_field(record["response"], ["status", "status_code"])
    try:
        return int(status)
    except (TypeError, ValueError):
        return None


def summarize_log(path):
    slow_paths = defaultdict(lambda: {"time": 0.0, "count": 0})
    error_paths = Counter()
    trace_counts = Counter()
    rpm = Counter()
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(hours=1)
    timestamp_found = False

    with open(path, "r", encoding="utf-8") as handle:
        for line in handle:
            record = parse_json_line(line)
            if not record:
                continue

            path_label = normalize_path(record)
            status = parse_status(record)
            duration = parse_duration(record)
            trace_id = get_field(record, ["trace_id", "traceId", "request_id", "trace-id"])
            timestamp = parse_timestamp(record)

            if timestamp is not None:
                timestamp_found = True
                minute_key = timestamp.replace(second=0, microsecond=0)
                if timestamp >= cutoff:
                    rpm[minute_key] += 1

            if path_label and duration is not None:
                slow_paths[path_label]["time"] += duration
                slow_paths[path_label]["count"] += 1

            if path_label and status is not None and 400 <= status < 600:
                error_paths[path_label] += 1

            if trace_id:
                trace_counts[str(trace_id)] += 1

    top_slow = sorted(
        (
            (path_label, values["time"] / values["count"], values["count"])
            for path_label, values in slow_paths.items()
            if values["count"]
        ),
        key=lambda item: item[1],
        reverse=True,
    )[:10]

    top_errors = error_paths.most_common(5)
    repeated_traces = [(trace, count) for trace, count in trace_counts.items() if count >= 20]
    repeated_traces.sort(key=lambda item: item[1], reverse=True)
    recent_rpm = sorted(rpm.items())

    return {
        "top_slow": top_slow,
        "top_errors": top_errors,
        "recent_rpm": recent_rpm,
        "repeated_traces": repeated_traces,
        "timestamp_found": timestamp_found,
    }


def print_section(title, rows, headers):
    print(f"\n{title}")
    print("-" * len(title))
    if not rows:
        print("No data available.")
        return

    widths = [max(len(str(cell)) for cell in column) for column in zip(*([headers] + rows))]
    template = "  " + "  ".join(f"{{:{w}}}" for w in widths)
    print(template.format(*headers))
    print(template.format(*["-" * w for w in widths]))
    for row in rows:
        print(template.format(*row))


def main():
    parser = argparse.ArgumentParser(description="Parse structured Conduit JSON access logs.")
    parser.add_argument("logfile", help="Path to the log file to analyze")
    args = parser.parse_args()

    summary = summarize_log(args.logfile)

    print_section(
        "Top 10 slowest endpoints by average response time",
        [
            (path_label, f"{avg:.3f}s", count)
            for path_label, avg, count in summary["top_slow"]
        ],
        ["Endpoint", "Avg Latency", "Samples"],
    )

    print_section(
        "Top 5 most frequent error paths (4xx + 5xx)",
        [(path_label, count) for path_label, count in summary["top_errors"]],
        ["Endpoint", "Error Count"],
    )

    if summary["timestamp_found"]:
        print_section(
            "Requests per minute for the last hour",
            [
                (ts.strftime("%Y-%m-%d %H:%M"), count)
                for ts, count in summary["recent_rpm"]
            ],
            ["Minute", "Requests"],
        )
    else:
        print("\nRequests per minute for the last hour")
        print("-----------------------------------")
        print("No timestamp data found in log lines.")

    print_section(
        "Trace IDs appearing 20+ times",
        summary["repeated_traces"],
        ["Trace ID", "Count"],
    )


if __name__ == "__main__":
    main()
