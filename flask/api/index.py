from flask import Flask, render_template, flash, request, redirect, url_for, send_file  
from flask_uploads import UploadSet, IMAGES, configure_uploads  
import os  
from PIL import Image, ImageFilter

app = Flask(__name__)  
app.config['UPLOAD_FOLDER'] = 'uploads'  
app.config['ALLOWED_EXTENSIONS'] = set(['jpg', 'jpeg', 'png', 'gif'])
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

@app.route('/')  
def welcome():  
    return render_template('welcome.html')

@app.route('/upload', methods=['POST'])  
def upload_file():  
    if 'file' not in request.files:  
        flash('请选择图片！')  
        return redirect(url_for('welcome'))

    file = request.files['file']
    if file.filename == '':  
        flash('请选择图片！')  
        return redirect(url_for('welcome'))

    filename = photos.save(file)
    upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)  
    image = Image.open(file.stream)  
    image_type = image.format

    # 在这里添加处理图片的逻辑，例如：  
    image = image.filter(ImageFilter.GaussianBlur(10))  # 模糊处理  
    image = image.point(lambda i: i * 0.5)  # 加噪处理  
    image = image.convert('L')  # 灰度化处理

    image.save(upload_path)  
    flash('图片上传成功！')  
    return redirect(url_for('welcome'))

@app.route('/download/<filename>')  
def download_file(filename):  
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)  
    if os.path.exists(file_path):  
        return send_file(file_path, mimetype='image/jpeg')  
    else:  
        flash('文件不存在！')  
        return redirect(url_for('welcome'))

if __name__ == '__main__':  
    app.run(debug=True)
