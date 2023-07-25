from flask import Flask, render_template, flash, request, redirect, url_for, send_file  
from flask_uploads import upload_files  
import os  
from PIL import Image

app = Flask(__name__)  
app.config['UPLOAD_FOLDER'] = 'uploads'  
app.config['ALLOWED_EXTENSIONS'] = ['*']

@app.route('/')  
def welcome():  
   return render_template('welcome.html')

@app.route('/upload', methods=['POST'])  
def upload_file():  
   uploads = upload_files('file', '.jpg,.jpeg,.png,.gif')  
   if uploads:  
       for upload in uploads:  
           filename = upload.filename  
           upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)  
           image = Image.open(upload.stream)  
           image_type = image.format

           # 在这里添加处理图片的逻辑，例如：  
           image = image.filter(ImageFilter.GaussianBlur(10))  # 模糊处理  
           image = image.point(lambda i: i * 0.5)  # 加噪处理  
           image = image.convert('L')  # 灰度化处理

           image.save(upload_path)  
           upload.save(upload_path)  
           flash('图片上传成功！')  
           return redirect(url_for('welcome'))  
   else:  
       flash('请选择图片！')  
       return redirect(url_for('welcome'))

@app.route('/download/<filename>')  
def download_file(filename):  
   file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)  
   if os.path.exists(file_path):  
       send_file(file_path, mimetype='image/jpeg')  
   else:  
       flash('文件不存在！')  
       return redirect(url_for('welcome'))

if __name__ == '__main__':  
   app.run(debug=True)  

