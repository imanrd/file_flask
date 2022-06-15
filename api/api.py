import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename
from . import key

app = Flask(__name__)

UPLOAD_FOLDER = '../data/'
ALLOWED_EXTENSIONS = {'csv'}
UPLOADS_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOADS_PATH

app.secret_key = key.secret_key
app.config['SESSION_TYPE'] = 'filesystem'
"""
یک سری فایل CSV روی دیسک یک سرور flask داریم، اینا یک سری عملیات روشون انجام میشه. 
Upload
List 
Delete 
Download 
Diagram 
Train
چهارتای اول که فکر کنم معلومه. 
برای دیاگرام اسم فایل و دو تا از ستون‌ها رو میگیره و یک تصویر برمیگردونه که نمودار بین اون ستون‌ها هست. 
برای train اسم سلام فایل و یکی از ستون‌ها رو به عنوان هدف آموزش و اسم یک روش آموزش رو میگیره و با scikit Learn آموزش میده و مدل رو با مقدار خطا برمیگردونه. 

فعلا خروجی همون صفحه apidocs که swagger خودش تولید میکنه باشه هم اوکی هست.
بعدا این رو گسترش میدیم


این یادم رفت 
لیست مدل‌هایی که میتونه آموزش بده هم باید برگردونیم. 

گسترش‌ها
یک celery همراهش باشه که آموزش روی اون انجام بشه
اسلام لازم داره که یک ماشین صف باشه مثلا rabbit mq
اینا همش میره روی داکر با docker compose

این امکان هم باید اضافه بشه که لیست مدل‌های آموزش داده شده رو بگیره
و بتونه نام یک مدل و تعدادی داده بده و پاسخ مدل رو برگردونه
"""


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/invalid_upload')
def index():
    return render_template('index.html')


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(url_for('index'))
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(url_for('index'))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('download_file', name=filename))
    return


@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)
