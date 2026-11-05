import os
from flask import Flask, Response, jsonify

app = Flask(__name__)


@app.route("/")
def index():
    html_content = """<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AWS EC2 Web Application - DevOps Lab 4</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1f2937, #111827);
            color: #f3f4f6;
            margin: 0;
            padding: 40px 20px;
            display: flex;
            justify-content: center;
        }
        .container {
            max-width: 700px;
            background-color: #1e293b;
            border-radius: 12px;
            padding: 30px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.5);
            border: 1px solid #334155;
        }
        h1 {
            color: #ff9900;
            margin-top: 0;
            border-bottom: 2px solid #334155;
            padding-bottom: 15px;
        }
        .badge {
            background-color: #10b981;
            color: white;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 0.9em;
            font-weight: bold;
        }
        .info-table {
            width: 100%;
            margin-top: 20px;
            border-collapse: collapse;
        }
        .info-table td {
            padding: 10px;
            border-bottom: 1px solid #334155;
        }
        .info-table td:first-child {
            font-weight: bold;
            color: #94a3b8;
            width: 40%;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>AWS EC2 Cloud Deployment <span class="badge">Online</span></h1>
        <p>Вебзастосунок успішно розгорнуто на віртуальному сервері Amazon Web Services.</p>
        <table class="info-table">
            <tr>
                <td>Лабораторна робота:</td>
                <td>№4 — Створення EC2-інстансу в AWS та ручне розгортання</td>
            </tr>
            <tr>
                <td>Виконав:</td>
                <td>студент групи М-25 Котенко Вадим</td>
            </tr>
            <tr>
                <td>Платформа:</td>
                <td>Amazon Web Services (AWS)</td>
            </tr>
            <tr>
                <td>Тип інстансу:</td>
                <td>t2.micro (AWS Free Tier)</td>
            </tr>
            <tr>
                <td>Операційна система:</td>
                <td>Ubuntu Server 22.04 LTS (Jammy Jellyfish)</td>
            </tr>
            <tr>
                <td>Вебсервер / WSGI:</td>
                <td>Gunicorn (порт 80 / HTTP)</td>
            </tr>
            <tr>
                <td>Статус сервісу:</td>
                <td>Healthy (200 OK)</td>
            </tr>
        </table>
    </div>
</body>
</html>
"""
    return Response(html_content, mimetype="text/html; charset=utf-8")


@app.route("/health")
def health():
    return jsonify(
        {
            "status": "healthy",
            "service": "aws-ec2-flask",
            "environment": "AWS EC2 t2.micro",
            "code": 200,
        }
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 80))
    app.run(host="0.0.0.0", port=port, debug=True)

