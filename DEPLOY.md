# 🚀 Render'da Deploy Qilish - Qo'llanma

## 📋 Qadamlar

### 1️⃣ GitHub'ga Repository Yaratish

1. **GitHub.com** ga kiring yoki qaydiylanish qiling
2. **+ → New repository** bosing
3. Repository nomini yozing: `telegram-media-bot`
4. **Create repository** bosing
5. Quyidagi commands'ni ishga tushiring:

```bash
cd C:\Users\usmon\WebstormProjects\untitled2

git init
git config user.name "Usmon"
git config user.email "your-email@gmail.com"

git add .
git commit -m "Initial commit: Telegram media downloader bot"

git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/telegram-media-bot.git
git push -u origin main
```

**ESLATMA**: `YOUR_USERNAME` ni o'zingizning GitHub username'ni qo'ying

---

### 2️⃣ Render'da Deploy Qilish

1. **Render.com** ga kiring (https://render.com)
2. **Sign up** yoki **Sign in**
3. **Dashboard** dan **Create +** bosing
4. **Web Service** yoki **Background Worker** tanlang

#### Option A: Web Service (Recommended)

```
Name: telegram-media-bot
Repository: https://github.com/YOUR_USERNAME/telegram-media-bot
Branch: main
Environment: Python 3
Build Command: pip install -r requirements.txt
Start Command: python bot.py

Environment Variables:
  TELEGRAM_BOT_TOKEN = 7596488118:AAFwv9P0Rftj3m328buWpfMo35zZiC81x70
```

#### Option B: Background Worker

```
Name: telegram-media-bot
Repository: https://github.com/YOUR_USERNAME/telegram-media-bot
Branch: main
Environment: Python 3
Build Command: pip install -r requirements.txt
Start Command: python bot.py

Environment Variables:
  TELEGRAM_BOT_TOKEN = 7596488118:AAFwv9P0Rftj3m328buWpfMo35zZiC81x70
```

5. **Create Web Service** / **Create Background Worker** bosing
6. Deploy boshlandi, kutib turing

---

### 3️⃣ Muammolarni Tuzatish

**❌ "FFmpeg not found" xatosi bilan qacha:**

Agar MP3 download error bersa, Render'da `ffmpeg` o'rnatish kerak.

`render.yaml` faylida quyidagini qo'shing:

```yaml
services:
  - type: web
    name: telegram-media-bot
    env: python
    buildCommand: |
      apt-get update && apt-get install -y ffmpeg
      pip install -r requirements.txt
    startCommand: python bot.py
```

**❌ "Module not found" xatosi:**

`requirements.txt` to'g'ri ekanligini tekshiring va qayta push qiling.

---

### 4️⃣ Render'da Logs Tekshirish

1. Render Dashboard'dan bot'ni tanlang
2. **Logs** tabini bosing
3. Errors tekshiring

---

## 📌 Har Doim Ishlash Uchun

Render Free plan'da 15 minutdan ko'p inactivity bo'lsa, service to'xtab ketadi.

**Solve qilish:** Paid plan'ga o'ting yoki cronjob orqali server'ni "uyandir"

---

## ✅ Deploy Tugallangach

Bot Telegram'da ishlashi kerak:
- Instagram URL yuboring
- YouTube URL yuboring  
- Qoshiq qidiruv qiling

---

**GitHub**: https://github.com/YOUR_USERNAME/telegram-media-bot
**Render**: https://dashboard.render.com

Savollar bor bo'lsa yozing! 🚀
