FROM python:3.9-slim-buster

# نصب پیش‌نیازهای سیستم
RUN apt-get update && \
    apt-get -qq -y install tesseract-ocr && \
    apt-get -qq -y install libtesseract-dev


# تنظیم محیط کار
WORKDIR /app

# کپی و نصب پکیج‌های پایتون در محیط مجازی
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# کپی کردن کل پروژه
COPY . .

# اجرای برنامه
CMD ["gunicorn", "app:app"]
