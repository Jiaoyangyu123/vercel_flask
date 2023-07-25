from flask import Flask, render_template
from flask_jinja2 import Jinja2Templates
import os
import sqlite3
import numpy as np
import cv2

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sample.db'
app.config['JINJA2_template_folder'] = 'templates'
templates = Jinja2Templates(app)

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/upload', methods=['POST'])
def upload():
    # 获取上传的图片
    file = request.files.get('image')
    if file:
        # 图片处理
        img = cv2.imread(file.stream)
        img_noisy = cv2.addWeighted(img, 0.1, np.zeros(img.shape), 0.1, 0)
        img_gray = cv2.cvtColor(img_noisy, cv2.COLOR_BGR2GRAY)
        img_blur = cv2.GaussianBlur(img_gray, (3, 3), 0)
        img_fuzzy = cv2.FuzzyCategorization(img_blur, 20, 0.7, 0.3, 20)
        # 保存处理后的图片
        file.save('processed.jpg')
    return render_template('upload.html', success=True)

if __name__ == '__main__':
    app.run(debug=True)
