THIS REPOSITORY IS OWNED BY @ahsanzizan on GitHub

# Instagram to Telegram Summary Bot

This Python script fetches the latest 5 posts from a public Instagram account and sends a summary (likes, comments, views, and caption preview) to a specified Telegram chat.

## Features

- Fetch insights from the 5 most recent posts of any public Instagram account
- Send a summary to a Telegram chat using a Telegram bot
- Supports both image and video posts
- Uses a pre-authenticated Instagram session to bypass login restrictions

---

## 🔧 Installation

### Requirements

- Python 3.8+
- pip (Python package installer)

### Install dependencies

```bash
pip install -r requirements.txt
```

**requirements.txt**

```
python-telegram-bot==20.0b1
instaloader
python-dotenv
```

---

## ⚙️ Environment Variables Setup

Create a `.env` file in the project root:

```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id
IG_USERNAME=instagram_username_to_scrape

IG_SESSION_USERNAME=your_ig_username
IG_CSRFTOKEN=your_csrftoken
IG_SESSIONID=your_sessionid
IG_DS_USER_ID=your_ds_user_id
IG_MID=your_mid_cookie
IG_IG_DID=your_ig_did_cookie
```

### How to Get Instagram Session Data

1. Log in to Instagram from your browser.
2. Open **Developer Tools > Application > Cookies**.
3. Copy the values of the following cookies:

   - `csrftoken`
   - `sessionid`
   - `ds_user_id`
   - `mid`
   - `ig_did`

4. Paste them into your `.env` file accordingly.

---

## ▶️ Running the Bot

To run it manually:

```bash
python main.py
```

---

## ⏱️ Schedule to Run Automatically Every X Hours

### On Windows

1. Open Task Scheduler.
2. Create a new task:

   - Trigger: Daily or Hourly
   - Action: `Start a program`
   - Program/script: `python`
   - Add arguments: `path\to\main.py`
   - Start in: `path\to\your\project`

### On Linux/macOS

Use `cron`:

```bash
crontab -e
```

Add a line like this to run every 6 hours:

```cron
0 */6 * * * /usr/bin/python3 /path/to/main.py
```

---

## 🧪 Development Notes

- Make sure the Instagram account is public
- Avoid spamming the Telegram API to prevent rate limits (this script uses `asyncio.sleep(1)`)
- If Instagram throws a 429 or 403 error, try changing the session cookies

---

## 📄 License

MIT License

---

## 🙋 FAQ

### What if the bot fails to load Instagram session?

Check that your cookie values are correct and not expired. You may need to log in to Instagram and get fresh cookies.

### Can I monitor multiple Instagram accounts?

Not currently, but you can easily modify the script to iterate over a list of usernames.

### What happens if the caption is too long?

Only the first 200 characters are shown with an ellipsis.

---

## 📬 Example Output

```
@instagram
https://www.instagram.com/p/Cxyz12345/
👍 Likes: 12,345
💬 Comments: 234
▶️ Views: 56,789
📝 This is the beginning of the caption that may be truncated if it's too long...
```

---

Feel free to fork and customize!
