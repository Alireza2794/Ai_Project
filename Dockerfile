FROM python:3.9-slim-buster

# نصب پیش‌نیازهای سیستم
RUN apt-get update && apt-get install -y \
    python \
    python-pip \
    python-venv \
    python-distutils \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

# تنظیم محیط کار
WORKDIR /app

# کپی و نصب پکیج‌های پایتون در محیط مجازی
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# کپی کردن کل پروژه
COPY . .

# اجرای برنامه
CMD ["gunicorn", "app:app"]
