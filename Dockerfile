FROM ubuntu:latest

# نصب پیش‌نیازهای سیستم
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

# تنظیم محیط کار
WORKDIR /app

# ایجاد و فعال‌سازی محیط مجازی
RUN python3 -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

# کپی و نصب پکیج‌های پایتون در محیط مجازی
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# کپی کردن کل پروژه
COPY . /app

# اجرای برنامه
CMD ["python3", "app.py"]
