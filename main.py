import os
import requests
import google.generativeai as genai
import asyncio
from telegram import Bot

# دریافت رمزها
TOKEN = os.getenv("TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

# تنظیم هوش مصنوعی
if GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)
    # از مدل فلش استفاده میکنیم که جدیده
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    print("⚠️ هشدار: کلید جمنای پیدا نشد!")

def get_latest_news():
    url = "https://min-api.cryptocompare.com/data/v2/news/?lang=EN"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        latest = data['Data'][0]
        return latest['title'], latest['body'], latest['url']
    except Exception as e:
        print(f"❌ خطا در دریافت خبر: {e}")
        return None, None, None

def ai_rewrite(title, body):
    if not GEMINI_KEY: return None
    print("🧠 هوش مصنوعی در حال نوشتن...")
    prompt = f"""
    You are a professional crypto journalist for a Persian Telegram channel.
    Rewrite the following news into exciting, engaging Persian (Farsi).
    Rules:
    1. Start with a catchy headline with emojis.
    2. Summarize the core message in 2-3 sentences.
    3. Tone: Casual, hype, professional.
    4. NO "According to report". Just the news.
    5. End with 3 viral hashtags.
    News Title: {title}
    News Body: {body}
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"❌ خطا در جمنای: {e}")
        return None

async def send_news():
    if not TOKEN:
        print("❌ توکن تلگرام نیست!")
        return
    title, body, url = get_latest_news()
    if title:
        print(f"✅ خبر دریافت شد: {title}")
        persian_text = ai_rewrite(title, body)
        if persian_text:
            msg = f"{persian_text}\n\n🔗 [مشاهده منبع خبر]({url})\n🆔 @gold\_price\_rls"
            bot = Bot(token=TOKEN)
            await bot.send_message(chat_id=CHANNEL_ID, text=msg, parse_mode='Markdown')
            print("🚀 پیام ارسال شد!")
        else:
            print("⚠️ هوش مصنوعی خروجی نداد.")
    else:
        print("⚠️ خبری پیدا نشد.")

if __name__ == '__main__':
    asyncio.run(send_news())
