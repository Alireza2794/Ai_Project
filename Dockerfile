FROM ubuntu:latest

# نصب Tesseract و پیش‌نیازها
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    python3 \
    python3-pip \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

# تنظیم محیط کار
COPY requirements.txt /app/requirements.txt
WORKDIR /app

# نصب پکیج‌های پایتون
RUN pip install --no-cache-dir -r requirements.txt

# تنظیم متغیر محیطی برای Tesseract
ENV TESSERACT_PATH=/usr/bin/tesseract

# کپی کردن کد پروژه
COPY . /app

# اجرای برنامه
CMD ["python3", "app.py"]
