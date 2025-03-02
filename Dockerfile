# استفاده از تصویر پایه با پایتون و Tesseract نصب‌شده
FROM ubuntu:latest

# نصب پیش‌نیازها
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# نصب پکیج‌های پایتون
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

# کپی کردن سورس پروژه
COPY . /app

# تنظیم Tesseract path
ENV TESSERACT_PATH=/usr/bin/tesseract

# اجرای برنامه
CMD ["python3", "app.py"]
