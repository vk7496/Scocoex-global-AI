# Scocoex-global-AI
In this project, we show how AI can help run and manage data
# SCOCOEX AI Core — دموی مفهومی

دموی ترکیبی پنج ماژول برای اجلاس SCOCOEX:

- 🎯 موتور هوشمند تطبیق B2B
- 💬 دستیار هوشمند چندزبانه (فارسی/انگلیسی)
- 📊 داشبورد مدیریتی زنده
- 📝 ثبت‌نام شرکت‌ها (فرم عمومی → Google Sheets)
- 🔐 پنل مدیریت (محافظت‌شده با رمز عبور، جست‌وجو/فیلتر بر اساس صنعت)

داده‌های ماژول تطبیق/چت/داشبورد نمایشی (mock) هستند. اما ماژول **ثبت‌نام**
و **پنل مدیریت** کاملاً واقعی کار می‌کنند: هر ثبت‌نام یا در Google Sheets
ذخیره می‌شود (در صورت تنظیم Secrets) یا در یک فایل CSV محلی — بدون اتصال
گوگل هم اپ خطا نمی‌دهد و کار می‌کند.

## اجرای محلی
```bash
pip install -r requirements.txt
streamlit run app.py
```
رمز پیش‌فرض پنل مدیریت در حالت محلی/بدون Secrets: `demo1234`

## دیپلوی روی Streamlit Cloud
1. این ریپو را روی GitHub پوش کن.
2. در Streamlit Cloud یک اپ جدید بساز و ریپو + فایل `app.py` را انتخاب کن.
3. برای اتصال واقعی به Google Sheets (بخش زیر) و تغییر رمز پنل مدیریت،
   از **Settings → Secrets** استفاده کن.

## اتصال به Google Sheets
1. در Google Cloud Console یک **Service Account** بساز و کلید JSON آن را دانلود کن.
2. یک Google Sheet جدید بساز و آن را با ایمیل `client_email` همان
   سرویس‌اکانت با نقش **Editor** به اشتراک بگذار (Share).
3. در Streamlit Cloud → Settings → Secrets، دقیقاً این ساختار را اضافه کن
   (مقادیر را از فایل JSON دانلودشده کپی کن):

   ```toml
   admin_password = "یک-رمز-قوی-اینجا"
   gsheet_key = "SPREADSHEET_ID_یا_URL_کامل_شیت"

   [gcp_service_account]
   type = "service_account"
   project_id = "..."
   private_key_id = "..."
   private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
   client_email = "...@...iam.gserviceaccount.com"
   client_id = "..."
   token_uri = "https://oauth2.googleapis.com/token"
   ```
4. بعد از ذخیره Secrets، اپ را Reboot کن. اگر اتصال درست باشد، نشانگر
   «● متصل به Google Sheets» در تب‌های «ثبت‌نام شرکت‌ها» و «پنل مدیریت»
   سبز می‌شود؛ در غیر این صورت اپ بدون خطا روی CSV محلی ادامه می‌دهد.
5. ورک‌شیت (اسمش `registrations` است و خودکار ساخته می‌شود) دقیقاً همان
   جایی است که تیم اجرایی SCOCOEX می‌تواند مستقیم در گوگل‌شیت هم داده‌ها
   را ببیند — بدون نیاز به باز کردن خود اپ.

## تفکیک صنعت‌ها
۱۰ صنعت رسمی اجلاس (دقیقاً مطابق سند خبرنامه SCOCOEX) به‌عنوان یک
لیست ثابت در `app.py` (متغیر `SECTORS`) تعریف شده و در فرم ثبت‌نام،
موتور تطبیق و فیلتر پنل مدیریت یکسان استفاده می‌شود — یعنی جست‌وجو و
فیلتر در پنل مدیریت همیشه بر همین تفکیک رسمی سوار است، نه یک لیست آزاد.

## ساختار پروژه
```
.
├── app.py                     # کل اپ (۵ تب / ۵ ماژول)
├── requirements.txt
├── assets/
│   └── scocoex_logo.png       # لوگوی رسمی SCOCOEX Global Week 2028
├── .streamlit/
│   └── config.toml            # تم رنگی (سرمه‌ای/طلایی) هماهنگ با برند
└── .gitignore
```
