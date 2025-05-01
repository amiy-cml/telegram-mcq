from flask import Flask, request
import requests
import os
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import pytz
import csv
import urllib.request

app = Flask(__name__)
scheduler = BackgroundScheduler()
scheduler.start()

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID")
SHEET_URL = os.environ.get("SHEET_URL") or "https://docs.google.com/spreadsheets/d/1ZOKOfJfjxPk7580S8fJf_A5piClZn8SxmS3_oAAbiTE/gviz/tq?tqx=out:csv&sheet=Sheet1"

def send_telegram_message(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHANNEL_ID, "text": msg, "parse_mode": "Markdown"}
    requests.post(url, data=data)

def send_telegram_quiz(correct_index):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPoll"
    data = {
        "chat_id": CHANNEL_ID,
        "question": "What's the answer to the above?",
        "options": ["A", "B", "C", "D", "E"],
        "type": "quiz",
        "correct_option_id": correct_index,
        "is_anonymous": False,
        "explanation": "Answer will be revealed in the next message!"
    }
    requests.post(url, json=data)

def fetch_today_question():
    try:
        with urllib.request.urlopen(SHEET_URL) as response:
            lines = [l.decode('utf-8') for l in response.readlines()]
            reader = csv.DictReader(lines)
            today = datetime.now(pytz.timezone("Asia/Kolkata")).strftime("%Y-%m-%d")
            for row in reader:
                if row['Date'].strip() == today:
                    return row
            return None
    except Exception as e:
        print("Error fetching today's question:", e)
        return None

def daily_post():
    q = fetch_today_question()
    if not q:
        send_telegram_message("No scheduled MCQ for today.")
        return

    question_text = f"*QID: {q['Question ID']}*\n\n{q['Question']}\n\n" +                     f"A. {q['Option A']}\nB. {q['Option B']}\nC. {q['Option C']}\n" +                     f"D. {q['Option D']}\nE. {q['Option E']}"
    send_telegram_message(question_text)

    answer_map = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4}
    correct_index = answer_map.get(q["Correct Answer"].strip().upper(), 0)
    send_telegram_quiz(correct_index)

    explanation = f"✅ *Correct Answer*: {q['Correct Answer']} \n\n*Explanation:* {q['Answer Explanation']}"
    send_telegram_message(explanation)

def schedule_daily():
    ist = pytz.timezone("Asia/Kolkata")
    now = datetime.now(ist)
    target = now.replace(hour=10, minute=0, second=0, microsecond=0)
    if now > target:
        target += timedelta(days=1)
    scheduler.add_job(daily_post, 'interval', days=1, next_run_time=target)

schedule_daily()

@app.route("/")
def home():
    return "Bot is running"

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    return "OK"
