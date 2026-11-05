from flask import Flask

app = Flask(__name__)

@app.get("/")
def index():
    return "Hello from Kubernetes\n", 200, {"Content-Type": "text/plain; charset=utf-8"}

@app.get("/healthz")
def health():
    return "ok\n", 200, {"Content-Type": "text/plain; charset=utf-8"}
