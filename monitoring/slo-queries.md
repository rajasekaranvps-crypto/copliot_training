# Conduit SLO PromQL Starter Queries

## 99.5% availability over 30 days
Query for the proportion of successful requests over the last 30 days.

```promql
1 - (
  sum(rate(http_requests_total{status=~"5.."}[30d]))
  / sum(rate(http_requests_total[30d]))
)
```

## p99 write endpoint latency under 500ms
Query the 99th percentile latency for write endpoints and compare to 0.5 seconds.

```promql
histogram_quantile(
  0.99,
  sum(rate(http_request_duration_seconds_bucket{path=~"/api/articles.*", method=~"POST|PUT|DELETE"}[5m])) by (le)
)
```

## Error budget burn rate for 5% monthly budget in 1 hour
Query the error budget burn rate for a 5% monthly error budget over one hour.

```promql
(
  sum(rate(http_requests_total{status=~"5.."}[1h]))
  / sum(rate(http_requests_total[30d]))
) / 0.05
```

> Notes:
> - These queries are starter examples for training and assume standard HTTP request metrics.
> - Adjust metric names and labels to match your Conduit instrumentation.
