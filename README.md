# Telegram MCQ AutoBot

A lightweight, fully automated Telegram bot that posts daily multiple-choice questions (MCQs) to your channel — perfect for medical revision, daily quizzes, or community learning.

## Features

- Posts one MCQ every day at **10:00 IST**
- Pulls question data **date-wise** from a **Google Sheet**
- Includes:
  - Full question message
  - Telegram quiz poll (`/quiz`) with correct answer pre-set
  - Follow-up message with detailed explanation

## Setup & Deployment (Railway)

### 1. Upload This Project

- Clone this repo or upload it to [https://railway.app](https://railway.app)
- Structure:
  ```
  .
  ├── main.py
  ├── requirements.txt
  └── .env.example
  ```

### 2. Set Environment Variables

Go to Railway > Project > Variables and set:

| Key          | Value                                                                 |
|--------------|-----------------------------------------------------------------------|
| `BOT_TOKEN`  | Your bot token from [@BotFather](https://t.me/BotFather)             |
| `CHANNEL_ID` | Your Telegram channel (e.g. `@yourchannelname`)                      |
| `SHEET_URL`  | Link to your Google Sheet in CSV format (see below)                  |

### 3. Format Your Google Sheet

Use this structure:

| Date       | Question ID | Question | Option A | Option B | Option C | Option D | Option E | Correct Answer | Answer Explanation |
|------------|-------------|----------|----------|----------|----------|----------|----------|----------------|---------------------|
| 2025-05-01 | Q001        | ...      | ...      | ...      | ...      | ...      | ...      | A              | ...                 |

**CSV link format:**
```
https://docs.google.com/spreadsheets/d/YOUR_ID/gviz/tq?tqx=out:csv&sheet=Sheet1
```

### 4. Set the Webhook

Once deployed, open this in your browser:

```
https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook?url=https://your-app.up.railway.app/<YOUR_BOT_TOKEN>
```

---

## Example Output

1. Full MCQ question posted to channel
2. Telegram quiz poll: "What's the answer to the above?"
3. Follow-up message: ✅ Correct Answer + explanation

---

## Built With

- Python
- Flask
- Apscheduler
- Google Sheets (as CMS)
- Telegram Bot API

---

## License

MIT — free for anyone to adapt, fork, and use.

---

> Created for the **Crack Medicine** community by [@yourgithub](https://github.com/yourgithub)
