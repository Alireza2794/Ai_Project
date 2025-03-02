from flask import Flask, render_template, request, jsonify
import pytesseract
import cv2
import re
import math
from langdetect import detect  
import os

app = Flask(__name__)

# تنظیم مسیر Tesseract
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

def detect_language(text_eng, text_fas):
    text = text_eng if len(text_eng.strip()) > len(text_fas.strip()) else text_fas
    try:
        lang = detect(text)
        return "eng" if lang == "en" else "fas"
    except:
        return "fas"  # پیش‌فرض فارسی

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

    # استخراج متن
    extracted_text = pytesseract.image_to_string(gray, lang="eng")

    # شناسایی عملیات ریاضی
    pattern = r'(\d+\.?\d*)\s?([+\-*/^()])\s?(\d+\.?\d*)'
    matches = re.findall(pattern, extracted_text)

    def solve_expression(expression):
        try:
            return eval(expression)
        except Exception:
            return "خطا در پردازش"

    results = []
    for match in matches:
        num1, operator, num2 = match
        expression = f"{num1} {operator} {num2}"
        results.append(f"{expression} = {solve_expression(expression)}")

    return jsonify({'results': results})

if __name__ == '__main__':
    app.run(debug=True)
