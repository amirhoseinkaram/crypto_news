import os
import requests

# دریافت کلید از گیت‌هاب
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

def list_models():
    if not GEMINI_KEY:
        print("❌ کلید GEMINI_API_KEY پیدا نشد!")
        return

    print("🔍 در حال دریافت لیست مدل‌های فعال برای شما...")
    
    # استفاده از لینک مستقیم API (بدون کتابخانه پایتون که ارور نده)
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={GEMINI_KEY}"
    
    try:
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print("\n📋 === لیست مدل‌های مجاز === ")
            found_any = False
            
            for model in data.get('models', []):
                # فقط مدل‌هایی که متن تولید میکنن رو نشون بده
                if 'generateContent' in model.get('supportedGenerationMethods', []):
                    # اسم مدل رو تمیز چاپ کن
                    print(f"✅ Name: {model['name']}")
                    print(f"   Display: {model['displayName']}")
                    print("-" * 30)
                    found_any = True
            
            if not found_any:
                print("❌ هیچ مدلی که قابلیت تولید متن داشته باشه پیدا نشد!")
        else:
            print(f"❌ ارور سمت گوگل: {response.text}")
            
    except Exception as e:
        print(f"❌ خطای ارتباطی: {e}")

if __name__ == '__main__':
    list_models()
