'''
# Course : CST 205
# Title : OCR using Python Libraries
# Abstract : We Create a Python Web Application using Tesseract which will Demonstrate OCR Functionality.
# Authors : Vighnesh Prabhu , Rajarshi Chatterjee and Hardik Kharpude.
# Date : 5/18/2022
# Work Division : The Project has 3 Parts : The GitHub Commits Demonstrate who did which Part.
# Rajarshi : Upload and Display Image 
# Vighnesh: OCR Functionality
# Hardik : HTML  Functionality

# GitHub - https://github.com/Kratosmsn11/cst205_project.git
# Trello - https://trello.com/invite/b/vB5YnYaL/673acf77c94c7872f63a2913ce1a74db/cst-205-team-7328

'''

from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
import os
from werkzeug.utils import secure_filename
import numpy as np
import pytesseract
import cv2
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = os.path.join(
    '.', 'Tesseract-OCR/tesseract')


def ocr_core(img):
    text = pytesseract.image_to_string(
        img, config='-c preserve_interword_spaces=1')
    return text


app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads/'

app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('Image Successfully Uploaded and Displayed Below')
        image = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        image = cv2.threshold(image, 100, 255, cv2.THRESH_BINARY)[1]
        image = cv2.GaussianBlur(image, (1, 1), 0)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = cv2.threshold(
        image, 200, 230, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        text = ocr_core(image)

        print(text)
        if len(text) == 0:
            text = 'No text detected from image'
        return render_template('index.html', filename=filename, text=text)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)


@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='uploads/' + filename), code=301)


def grayscale(img):
    new_list = [((a[0]+a[1]+a[2])//3, ) * 3 for a in img.getdata()]
    img.putdata(new_list)
    img.show()


if __name__ == "__main__":
    app.run()
