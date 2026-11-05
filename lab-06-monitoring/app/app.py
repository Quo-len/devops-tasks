import random
import time

from flask import Flask, Response, g, request
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Gauge, Histogram, generate_latest

app = Flask(__name__)
REQUESTS = Counter("app_requests_total", "Total HTTP requests", ["method", "endpoint", "status"])
LATENCY = Histogram(
    "app_request_duration_seconds", "Time inside Flask (excludes Gunicorn queue)",
    ["endpoint"], buckets=[0.05, 0.1, 0.25, 0.5, 1, 2.5, 5],
)
IN_PROGRESS = Gauge("app_requests_in_progress", "Requests inside Flask, including metrics scrape")


@app.before_request
def start_timer():
    g.started_at = time.perf_counter()
    IN_PROGRESS.inc()


@app.after_request
def record_metrics(response):
    if request.path != "/metrics":
        endpoint = request.url_rule.rule if request.url_rule else "unknown"
        LATENCY.labels(endpoint).observe(time.perf_counter() - g.started_at)
        REQUESTS.labels(request.method, endpoint, str(response.status_code)).inc()
    return response


@app.teardown_request
def finish_request(error=None):
    if g.pop("started_at", None) is not None:
        IN_PROGRESS.dec()


@app.get("/")
def index():
    return "Hello, monitoring!\n"


@app.get("/slow")
def slow():
    time.sleep(random.uniform(0.2, 2.0))
    return "Slow response\n"


@app.get("/error")
def error():
    if random.random() < 0.5:
        return "Internal error\n", 500
    return "Lucky this time\n"


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), content_type=CONTENT_TYPE_LATEST)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
