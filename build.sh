#/!/bin/bash
python -m venv live-score-notifier
source live-score-notifier/bin/activate
pip install --upgrade pip
pip install requests
pip install bs4
pip install notify-py
python3 src/main.py
