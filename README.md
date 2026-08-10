# 🎬 Telegram Media Yuklab Olish Boti

Instagram, YouTube va Qoshiq qidiruv uchun Telegram boti.

## ✨ Xususiyatlari

- 📸 **Instagram** videodan/rasmdan yuklab olish
- 🎥 **YouTube** video → 1080p yoki MP3 formatda
- 🎵 **Qoshiq qidiruv** nomi va artistni qidirishda

## 🚀 O'rnatish

### 1️⃣ Telegram Bot Yaratish

1. Telegramda `@BotFather` bilan yozning
2. `/newbot` komandasi bilan yangi bot yarating
3. Token olding

### 2️⃣ Proyektni O'rnatish

```bash
# Python 3.8+ kerak
python --version

# Librarylarni o'rnatish
pip install -r requirements.txt

# .env faylini sozlash
# .env faylida TOKEN ni yozing
echo "TELEGRAM_BOT_TOKEN=YOUR_TOKEN" > .env
```

### 3️⃣ Botni Ishga Tushirish

**Linux/Mac:**
```bash
bash run.sh
```

**Windows (PowerShell):**
```powershell
python bot.py
```

## 📖 Foydalanish

### Instagram Video
```
Botga URL yubor:
https://www.instagram.com/p/ABC123...
```

### YouTube Video
```
Botga URL yubor:
https://www.youtube.com/watch?v=ABC123
👇 1080p yoki MP3 tanlash knopkasi chiqadi
```

### Qoshiq Qidiruv
```
Format: Nomi - Artist

Misollar:
✅ Usmonali - Chuqur Muhabbat
✅ Bilal Soniy - Sevma Meni
```

## 📦 Serverga Deploy Qilish

### Ubuntu/Debian Server

```bash
# SSH orqali serverga kirish
ssh user@server_ip

# Proyektni klonlashtirish yoki fayl yuklash
# Git bo'lsa:
git clone YOUR_REPO_URL
cd untitled2

# Yoki fayllarni ko'chirish:
scp -r untitled2/* user@server_ip:/home/user/bot/

# Serverda
cd /home/user/bot
pip install -r requirements.txt
```

### Systemd Service (avtomatik ishga tushishi uchun)

```bash
sudo nano /etc/systemd/system/telegram-bot.service
```

Quyidagini yozing:
```ini
[Unit]
Description=Telegram Media Bot
After=network.target

[Service]
Type=simple
User=user
WorkingDirectory=/home/user/bot
Environment="PATH=/home/user/bot/venv/bin"
ExecStart=/usr/bin/python3 /home/user/bot/bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Ishga tushirish:
```bash
sudo systemctl daemon-reload
sudo systemctl enable telegram-bot
sudo systemctl start telegram-bot

# Status tekshirish
sudo systemctl status telegram-bot
```

## 🔑 Muhim Qaydlar

1. **Token xavfsizligi**: TOKEN ni .env faylida saqlang
2. **Instagram**: Bazan Instagram blocks bo'lishi mumkin, proxy ishlatish kerak
3. **YouTube**: FFmpeg o'rnatish kerak MP3 uchun
   - Ubuntu: `sudo apt-get install ffmpeg`
   - Mac: `brew install ffmpeg`
   - Windows: choco orqali yoki yuklash

## 🐛 Muammolar

### FFmpeg yo'q
```bash
# Ubuntu
sudo apt-get install ffmpeg

# Mac
brew install ffmpeg

# Windows (Chocolatey)
choco install ffmpeg
```

### Instagram xatosi
- Proxy yoki VPN ishlatib ko'ring
- Session-based login qo'llanish mumkin

## 💡 Takmini

- Database (MongoDB/PostgreSQL) bilan qidiruvlarni saqlash
- Admin panel qo'shish
- Tarjima qo'shish (multi-language)
- Admin log'i

## 📝 Litsenziya

MIT

---

**Savollar? GitHub Issues ochib yozing yoki meni bog'lang!** 🚀
