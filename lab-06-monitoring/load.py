"""Standard-library load generator. Ctrl+C stops cleanly; summaries every 5 seconds."""
import argparse
from collections import Counter, defaultdict
import math
import random
import threading
import time
import urllib.error
import urllib.request


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("duration", nargs="?", type=int, default=600)
    parser.add_argument("threads", nargs="?", type=int, default=10)
    parser.add_argument("--error-heavy", action="store_true", help="80%% /error for the optional alert experiment")
    parser.add_argument("--url", default="http://127.0.0.1:5000")
    args = parser.parse_args()
    if args.duration <= 0 or args.threads <= 0:
        parser.error("duration and threads must be positive")
    paths = ["/"] * 6 + ["/slow"] * 2 + ["/error"] * 2
    if args.error_heavy:
        paths = ["/"] + ["/slow"] + ["/error"] * 8
    stop = threading.Event()
    lock = threading.Lock()
    totals, interval, latencies = Counter(), Counter(), defaultdict(list)
    deadline = time.monotonic() + args.duration

    def worker():
        while not stop.is_set() and time.monotonic() < deadline:
            path = random.choice(paths)
            started = time.perf_counter()
            try:
                with urllib.request.urlopen(args.url + path, timeout=10) as response:
                    response.read()
                    status = str(response.status)
            except urllib.error.HTTPError as error:
                status = str(error.code)
                error.close()
            except (OSError, urllib.error.URLError):
                status = "fail"
            elapsed = time.perf_counter() - started
            with lock:
                totals[status] += 1
                interval[status] += 1
                latencies[path].append(elapsed)
            stop.wait(random.uniform(0.05, 0.3))

    def summary():
        with lock:
            counts = dict(interval)
            p95 = {p: round(sorted(v)[math.ceil(0.95 * len(v)) - 1], 3) for p, v in latencies.items() if v}
            interval.clear()
            latencies.clear()
        print(f"Last interval: HTTP={counts} client_p95_seconds={p95}", flush=True)

    print(f"Load: {args.threads} threads, {args.duration}s, URL={args.url}, error_heavy={args.error_heavy}", flush=True)
    pool = [threading.Thread(target=worker) for _ in range(args.threads)]
    for thread in pool:
        thread.start()
    try:
        while time.monotonic() < deadline:
            stop.wait(min(5, max(0, deadline - time.monotonic())))
            summary()
    except KeyboardInterrupt:
        print("Stopping; waiting for in-flight requests (up to 10s)...", flush=True)
    finally:
        stop.set()
        for thread in pool:
            thread.join()
        summary()
        print(f"Total HTTP responses / failures: {dict(totals)}", flush=True)


if __name__ == "__main__":
    main()
