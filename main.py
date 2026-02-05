import os
import requests
import asyncio
from telegram import Bot

# دریافت رمزها
TOKEN = os.getenv("TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

def get_latest_news():
    """دریافت خبر از سایت کریپتو"""
    url = "https://min-api.cryptocompare.com/data/v2/news/?lang=EN"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        if data.get('Data'):
            latest = data['Data'][0]
            return latest['title'], latest['body'], latest['url']
        return None, None, None
    except Exception as e:
        print(f"❌ خطا در دریافت خبر: {e}")
        return None, None, None

def ai_rewrite(title, body):
    """ترجمه با هوش مصنوعی (مدل Gemini 2.5 Flash)"""
    if not GEMINI_KEY:
        print("⚠️ کلید جمنای نیست!")
        return None

    print(f"🧠 هوش مصنوعی (Gemini 2.5) در حال فکر کردن...")
    
    # استفاده از مدل جدید که توی لیستت بود
    model_name = "gemini-2.5-flash" 
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={GEMINI_KEY}"
    
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
    
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    
    try:
        # ارسال درخواست مستقیم (بدون نیاز به کتابخانه)
        response = requests.post(api_url, json=payload, headers={'Content-Type': 'application/json'}, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            # استخراج متن از پاسخ جیسون
            return result['candidates'][0]['content']['parts'][0]['text']
        else:
            print(f"❌ خطای گوگل ({response.status_code}): {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ خطا در ارتباط با هوش مصنوعی: {e}")
        return None

async def send_news():
    if not TOKEN:
        print("❌ توکن تلگرام نیست!")
        return

    title, body, url = get_latest_news()
    
    if title:
        print(f"✅ خبر دریافت شد: {title}")
        
        # ارسال به هوش مصنوعی
        persian_text = ai_rewrite(title, body)
        
        if persian_text:
            # آماده‌سازی پیام تلگرام
            # بک‌اسلش قبل از آیدی برای جلوگیری از ایتالیک شدن
            msg = f"{persian_text}\n\n🔗 [لینک منبع]({url})\n🆔 @gold\_price\_rls"
            
            bot = Bot(token=TOKEN)
            await bot.send_message(chat_id=CHANNEL_ID, text=msg, parse_mode='Markdown')
            print("🚀 پیام با موفقیت ارسال شد!")
        else:
            print("⚠️ هوش مصنوعی خروجی نداد.")
    else:
        print("⚠️ خبری پیدا نشد.")

if __name__ == '__main__':
    asyncio.run(send_news())
