#!/usr/bin/env python3
"""
Synthetic monitor for Conduit application.
Runs a synthetic transaction every 60 seconds:
- Register a user
- Create an article
- Fetch the article
- Delete the article
Records per-step latency to metrics.csv.
Exits cleanly on SIGINT.
"""

import time
import signal
import sys
import csv
import urllib.request
import urllib.error
import json

# Configuration
BASE_URL = "http://localhost:8000/api"
CSV_FILE = "metrics.csv"

# Global flag for clean exit
running = True

def signal_handler(signum, frame):
    global running
    print("\nReceived SIGINT. Exiting cleanly...")
    running = False

def register_user():
    """Register a new user and return the auth token."""
    timestamp = str(int(time.time()))
    user_data = {
        "user": {
            "username": f"synthetic_user_{timestamp}",
            "email": f"synthetic_{timestamp}@example.com",
            "password": "password123"
        }
    }
    data = json.dumps(user_data).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/users", data=data, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result["user"]["token"]
    except urllib.error.HTTPError as e:
        raise Exception(f"Registration failed: {e.read().decode()}")

def login_user(email, password):
    """Login and return auth token."""
    login_data = {
        "user": {
            "email": email,
            "password": password
        }
    }
    data = json.dumps(login_data).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/users/login", data=data, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result["user"]["token"]
    except urllib.error.HTTPError as e:
        raise Exception(f"Login failed: {e.read().decode()}")

def create_article(token):
    """Create an article and return its slug."""
    timestamp = str(int(time.time()))
    article_data = {
        "article": {
            "title": f"Synthetic Article {timestamp}",
            "description": "A test article created by synthetic monitor",
            "body": "This is a synthetic article body for testing purposes.",
            "tagList": ["synthetic", "test"]
        }
    }
    data = json.dumps(article_data).encode('utf-8')
    headers = {"Authorization": f"Token {token}", 'Content-Type': 'application/json'}
    req = urllib.request.Request(f"{BASE_URL}/articles", data=data, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result["article"]["slug"]
    except urllib.error.HTTPError as e:
        raise Exception(f"Create article failed: {e.read().decode()}")

def fetch_article(token, slug):
    """Fetch the article by slug."""
    headers = {"Authorization": f"Token {token}"}
    req = urllib.request.Request(f"{BASE_URL}/articles/{slug}", headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result["article"]
    except urllib.error.HTTPError as e:
        raise Exception(f"Fetch article failed: {e.read().decode()}")

def delete_article(token, slug):
    """Delete the article by slug."""
    headers = {"Authorization": f"Token {token}"}
    req = urllib.request.Request(f"{BASE_URL}/articles/{slug}", headers=headers, method='DELETE')
    try:
        with urllib.request.urlopen(req) as response:
            pass  # DELETE usually returns 204
    except urllib.error.HTTPError as e:
        raise Exception(f"Delete article failed: {e.read().decode()}")

def run_synthetic_transaction():
    """Run the full synthetic transaction and record latencies."""
    latencies = {}
    start_time = time.time()

    try:
        # Step 1: Register user
        step_start = time.time()
        token = register_user()
        latencies["register_user"] = time.time() - step_start

        # Step 2: Create article
        step_start = time.time()
        slug = create_article(token)
        latencies["create_article"] = time.time() - step_start

        # Step 3: Fetch article
        step_start = time.time()
        fetch_article(token, slug)
        latencies["fetch_article"] = time.time() - step_start

        # Step 4: Delete article
        step_start = time.time()
        delete_article(token, slug)
        latencies["delete_article"] = time.time() - step_start

        # Record to CSV
        with open(CSV_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time))
            for step, latency in latencies.items():
                writer.writerow([timestamp, step, f"{latency:.3f}"])

        print(f"Transaction completed successfully at {timestamp}")

    except (urllib.error.HTTPError, urllib.error.URLError) as e:
        print(f"Transaction failed: {e}")

def main():
    # Set up signal handler for clean exit
    signal.signal(signal.SIGINT, signal_handler)

    # Initialize CSV file with headers if it doesn't exist
    try:
        with open(CSV_FILE, mode='x', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["timestamp", "step", "latency_seconds"])
    except FileExistsError:
        pass  # File already exists

    print("Starting synthetic monitor. Press Ctrl+C to stop.")

    while running:
        run_synthetic_transaction()
        time.sleep(60)

    print("Synthetic monitor stopped.")

if __name__ == "__main__":
    main()