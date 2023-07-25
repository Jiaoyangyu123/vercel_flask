from flask import Flask, render_template, request, send_file
from PIL import Image
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    # 获取上传的文件
    file = request.files['image']
    
    # 读取图像
    img = Image.open(file)
    
    # 处理图像（这里只是一个示例，您可以根据需要进行修改）
    img = img.convert('L')  # 灰度化
    
    # 保存处理后的图像到内存中
    img_io = io.BytesIO()
    img.save(img_io, 'JPEG')
    img_io.seek(0)
    
    # 返回处理后的图像给用户下载
    return send_file(img_io, mimetype='image/jpeg', as_attachment=True, attachment_filename='processed_image.jpg')

if __name__ == '__main__':
    app.run()
