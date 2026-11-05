#!/bin/bash
# Script for automatic server provisioning on AWS EC2 (Ubuntu 22.04 LTS)
set -e

echo "=========================================================="
echo " Starting setup on AWS EC2 Ubuntu instance                "
echo "=========================================================="

# 1. Update system packages
echo "--> 1. Updating APT package lists..."
sudo apt update -y
sudo apt upgrade -y

# 2. Install essential tools: Python 3, pip, git, curl
echo "--> 2. Installing Python 3, pip, venv and Git..."
sudo apt install -y python3 python3-pip python3-venv git curl

# 3. Install Python dependencies
echo "--> 3. Installing Python requirements (Flask, Gunicorn)..."
sudo pip3 install -r requirements.txt

# 4. Configure and start systemd background service
echo "--> 4. Configuring systemd service for Gunicorn..."
if [ -f "flask-app.service" ]; then
    sudo cp flask-app.service /etc/systemd/system/
    sudo systemctl daemon-reload
    sudo systemctl enable flask-app
    sudo systemctl restart flask-app
    echo "--> Checking systemd status:"
    sudo systemctl status flask-app --no-pager
    echo "=========================================================="
    echo " SUCCESS: Flask app is running as a systemd service on port 80!"
    echo " Open http://$(curl -s http://checkip.amazonaws.com) in browser."
    echo "=========================================================="
else
    echo "flask-app.service not found, starting directly via Gunicorn:"
    sudo gunicorn -b 0.0.0.0:80 app:app
fi

