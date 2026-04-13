# ⚡ Quick Start Guide

Get ThreatFeed Dashboard running in **5 minutes**!

---

## Step 1: Get API Keys (5 min)

### AbuseIPDB (REQUIRED)
1. Visit: https://www.abuseipdb.com/api
2. Sign up (free)
3. Click "API" → Copy your key

### Telegram Bot (REQUIRED)
1. Open Telegram
2. Search: **@BotFather**
3. Send: `/newbot`
4. Follow prompts, copy token
5. Search: **@userinfobot**
6. Send: `/start`
7. Copy your Chat ID

---

## Step 2: Setup (30 seconds)

```bash
# Install dependencies
pip install -r requirements.txt

# Create config file
cp .env.example .env

# Edit with your keys
nano .env
```

Paste in `.env`:
```
ABUSEIPDB_API_KEY=your_abuseipdb_key_here
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_chat_id_number
```

Save and exit (Ctrl+X, Y, Enter)

---

## Step 3: Run (10 seconds)

```bash
# Collect threats
python main.py

# Start dashboard
python app.py
```

**Open browser:** http://localhost:5000

---

## 🎉 Done!

You should see:
- ✅ Threats in your database
- ✅ Dashboard showing statistics
- ✅ Telegram alert with summary

---

## 🤖 Automate with GitHub Actions

1. **Push to GitHub:**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/USERNAME/threatfeed-dashboard.git
git push -u origin main
```

2. **Add secrets** (Settings → Secrets and variables → Actions):
   - `ABUSEIPDB_API_KEY`
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`

3. **Enable Actions** → Done! Runs every hour automatically

---

## 🆘 Need Help?

**Telegram not working?**
- Start your bot: Send `/start` to your bot
- Verify chat ID with @userinfobot

**No threats showing?**
- Run `python main.py` first
- Check console for errors
- Verify API keys in `.env`

**Dashboard won't start?**
- Install Flask: `pip install flask`
- Check port 5000 is free

---

## 📚 Next Steps

- Read full [README.md](README.md)
- Customize thresholds in `config.py`
- Add more data sources
- Deploy to cloud (Heroku, DigitalOcean, AWS)

---

**Questions?** Open an issue on GitHub!
