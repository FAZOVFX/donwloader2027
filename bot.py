import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from telegram.constants import ChatAction
import yt_dlp
import requests
from urllib.parse import urlparse

# Loglarni sozlash
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# TOKEN ni environment variabledan olish
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')

# Instagram yuklab olish
async def download_instagram(url: str) -> str:
    try:
        # Instagram API requests orqali
        response = requests.get(url)
        if response.status_code == 200:
            # Instagram video URL'sini extract qilish
            if 'instagram.com/p/' in url or 'instagram.com/reel/' in url:
                return url  # Direct link o'rniga API response berish
        return None
    except Exception as e:
        logger.error(f"Instagram download xatosi: {e}")
        return None

# YouTube yuklab olish
def download_youtube(url: str, format_type: str = 'best') -> str:
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'format': 'best[height<=1080]' if format_type == '1080p' else 'bestaudio/best',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }] if format_type == 'mp3' else []
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return info.get('id')
    except Exception as e:
        logger.error(f"YouTube download xatosi: {e}")
        return None

# Qoshiq qidiruv (Spotify API)
async def search_song(song_name: str, artist_name: str) -> list:
    try:
        search_query = f"{song_name} {artist_name}"
        url = "https://api.spotify.com/v1/search"
        
        # Spotify API uchun token kerak. Simple approach - YouTube Search API ishlatamiz
        youtube_search_url = f"https://www.youtube.com/results?search_query={song_name}+{artist_name}"
        
        # Alternativ: Deezer API
        deezer_url = "https://api.deezer.com/search"
        params = {'q': f"{song_name} {artist_name}"}
        response = requests.get(deezer_url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            tracks = data.get('data', [])[:5]
            return tracks
        return []
    except Exception as e:
        logger.error(f"Qoshiq qidiruv xatosi: {e}")
        return []

# /start komanda
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = """
🎬 **Instagram, YouTube va Qoshiq Yuklab Olish Boti**

Qabul qiladi:
✅ Instagram video/rasm URL si
✅ YouTube video URL si
✅ Qoshiq nomi va artist nomi (qidiruv)

Misollar:
📸 Instagram: https://www.instagram.com/p/ABC123...
🎥 YouTube: https://www.youtube.com/watch?v=ABC123...
🎵 Qoshiq: Usmonali - Chuqur Muhabbat

Yozing va boshlaylik! 🚀
    """
    await update.message.reply_text(message, parse_mode='Markdown')

# Asosiy xabar handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text
    chat_id = update.message.chat_id
    
    await context.bot.send_chat_action(chat_id, ChatAction.TYPING)
    
    # Instagram URL tekshirish
    if 'instagram.com' in text:
        await update.message.reply_text("📸 Instagram videodan yuklab olyapman...")
        video_url = await download_instagram(text)
        if video_url:
            try:
                await update.message.reply_video(video_url)
            except Exception as e:
                await update.message.reply_text(f"❌ Xato: {str(e)}")
        else:
            await update.message.reply_text("❌ Instagram videodan yuklab olib bo'lmadi")
    
    # YouTube URL tekshirish
    elif 'youtube.com' in text or 'youtu.be' in text:
        keyboard = [
            [
                InlineKeyboardButton("🎥 1080p Video", callback_data='youtube_1080p'),
                InlineKeyboardButton("🎵 MP3 Audio", callback_data='youtube_mp3')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.user_data['youtube_url'] = text
        await update.message.reply_text(
            "📥 Format tanlang:",
            reply_markup=reply_markup
        )
    
    # Qoshiq qidiruv (format: "Nomi - Artist")
    elif ' - ' in text or ' 🎵 ' in text:
        parts = text.replace('🎵', '').split(' - ')
        if len(parts) == 2:
            song_name = parts[0].strip()
            artist_name = parts[1].strip()
            
            await update.message.reply_text(f"🔍 Qidiruv: {song_name} - {artist_name}...")
            
            tracks = await search_song(song_name, artist_name)
            
            if tracks:
                message = "🎵 **Natijalar:**\n\n"
                for i, track in enumerate(tracks, 1):
                    title = track.get('title', 'Noma\'lum')
                    artist = track.get('artist', {}).get('name', 'Noma\'lum')
                    link = track.get('link', '')
                    message += f"{i}. {title}\n   👤 {artist}\n"
                
                await update.message.reply_text(message, parse_mode='Markdown')
            else:
                await update.message.reply_text("❌ Qoshiq topilmadi")
        else:
            await update.message.reply_text(
                "❓ Noto'g'ri format.\n\nQoshiqni qidiruv uchun: **Nomi - Artist**\n\nMisollar:\n• Usmonali - Chuqur Muhabbat\n• Uzbekiston - Qo'shiq"
            )
    else:
        await update.message.reply_text(
            "❓ URL yoki qoshiq nomi kiritish kerak.\n\n"
            "✅ Instagram URL\n"
            "✅ YouTube URL\n"
            "✅ Qoshiq: Nomi - Artist"
        )

# Button callback handler
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    youtube_url = context.user_data.get('youtube_url')
    if not youtube_url:
        await query.edit_message_text("❌ URL topilmadi. Qayta urinib ko'ring")
        return
    
    if query.data == 'youtube_1080p':
        await query.edit_message_text("📥 1080p yuklab olyapman...")
        download_youtube(youtube_url, '1080p')
        await query.message.reply_document(
            document=open(f'downloads/video.mp4', 'rb'),
            caption="✅ 1080p video"
        )
    
    elif query.data == 'youtube_mp3':
        await query.edit_message_text("📥 MP3 yuklab olyapman...")
        download_youtube(youtube_url, 'mp3')
        await query.message.reply_audio(
            audio=open(f'downloads/audio.mp3', 'rb'),
            caption="✅ MP3 audio"
        )

# Asosiy funksiya
async def main() -> None:
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CallbackQueryHandler(button_callback))
    
    print("🤖 Bot ishga tushdi...")
    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
