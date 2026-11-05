import os
from flask import Flask, Response

app = Flask(__name__)
GREETING = "Hello from Render! Група М-25."


@app.get("/")
def home():
    student = os.environ.get("STUDENT_NAME", "невідомий студент")
    return Response(
        f"{GREETING} Застосунок розгорнув: {student}\n",
        content_type="text/plain; charset=utf-8",
    )


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    # Windows development server. Render uses Gunicorn in production.
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="127.0.0.1", port=port, debug=True)
