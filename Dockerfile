FROM ubuntu:latest

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

# ایجاد و فعال‌سازی محیط مجازی
RUN python -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

# کپی و نصب پکیج‌های پایتون در محیط مجازی
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip setuptools
RUN pip install --no-cache-dir -r requirements.txt

# کپی کردن کل پروژه
COPY . /app

# اجرای برنامه
CMD ["python", "app.py"]
