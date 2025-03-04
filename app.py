from flask import Flask, render_template, request, jsonify
import pytesseract
import cv2
import re
import math
from langdetect import detect  
import os

app = Flask(__name__)

# تنظیم مسیر Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def detect_language(text_eng, text_fas):
    text = text_eng if len(text_eng.strip()) > len(text_fas.strip()) else text_fas
    try:
        lang = detect(text)
        return "eng" if lang == "en" else "fas"
    except:
        return "fas"  # پیش‌فرض فارسی

def persian_to_english_numbers(text):
    mapping = {
        '۰': '0', '۱': '1', '۲': '2', '۳': '3', '۴': '4',
        '۵': '5', '۶': '6', '۷': '7', '۸': '8', '۹': '9',
        '٠': '0', '١': '1', '٢': '2', '٣': '3', '٤': '4',
        '٥': '5', '٦': '6', '٧': '7', '٨': '8', '٩': '9'
    }
    return ''.join(mapping.get(ch, ch) for ch in text)



@app.route('/')
def index():
    return render_template('index.html')

# استخراج متن از تصویر
@app.route('/extract_text', methods=['POST'])
def extract_text():
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    # پردازش تصویر
    image_path = 'uploaded_image.jpg'
    file.save(image_path)
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # استخراج متن
    text_eng = pytesseract.image_to_string(gray, lang="eng")
    text_fas = pytesseract.image_to_string(gray, lang="fas")
    lang = detect_language(text_eng, text_fas)
    extracted_text = pytesseract.image_to_string(gray, lang=lang)

    return jsonify({'extracted_text': extracted_text})

# حل معادلات ریاضی
@app.route('/solve_math', methods=['POST'])
def solve_math():
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    # پردازش تصویر
    image_path = 'uploaded_image.jpg'
    file.save(image_path)
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    gray = clahe.apply(gray)
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]


    # استخراج متن
    extracted_text = pytesseract.image_to_string(gray, lang="eng+fas")

    # جایگزینی "÷" با "/" و حذف فاصله‌ها
    extracted_text = extracted_text.replace("÷", "/").replace(" ", "")

    # تبدیل اعداد فارسی به انگلیسی
    extracted_text = persian_to_english_numbers(extracted_text)


    # اگر OCR به اشتباه علامت تقسیم را به "+" تبدیل کرده باشد، اصلاح می‌کنیم.
    extracted_text = re.sub(r'(\d+)\+(\d+\()', r'\1/\2', extracted_text)

    # اصلاح ضرب ضمنی: تبدیل "digit(" به "digit*(" (مثلاً 2(2+2) به 2*(2+2))
    extracted_text = re.sub(r'(\d)\(', r'\1*(', extracted_text)

    # شناسایی عملیات ریاضی با یک الگوی ساده
    pattern = r'[\d+\-*/^().]+'
    matches = re.findall(pattern, extracted_text)

    def solve_expression(expression):
        try:
            # ارزیابی عبارت به‌صورت ایمن
            result = eval(expression, {"__builtins__": None}, {})
            result = int(result) if result.is_integer() else result

            return result
        except Exception:
            return "خطا در پردازش"

    results = []
    for expression in matches:
        results.append(f"{expression} = {solve_expression(expression)}")

    return jsonify({'results': results})

if __name__ == '__main__':
    app.run(debug=True)
