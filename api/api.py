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
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(url_for('index'))
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            # return redirect(request.url)
            return redirect(url_for('index'))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('download_file', name=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)


'''


def get_all_pets():  # noqa: E501
    """Gets all pets in the store

     # noqa: E501


    :rtype: Pets
    """
    pets = pets.get_all_pets()
    pets_in_store = []
    for pet in pets:
        current_pet = Pet(id=pet["id"], breed=pet["breed"], name=pet["name"], price=pet["price"])
        pets_in_store.append(current_pet)

    return pets_in_store, 200


def get_pet(pet_id):  # noqa: E501
    """Get a pet in the store

     # noqa: E501

    :param pet_id: The id of the pet to retrieve
    :type pet_id: str

    :rtype: Pet
    """
    try:
        pet = pets.get_pet(pet_id)
        response = Pet(id=pet.id, breed=pet.breed, name=pet.name, price=pet.price), 200
    except KeyError:
        response = {}, 404

    return response


def remove_pet(pet_id):  # noqa: E501
    """Remove a pet in the store

     # noqa: E501

    :param pet_id: The id of the pet to remove from the store
    :type pet_id: str

    :rtype: None
    """
    try:
        pets.remove_pet(pet_id)
        response = {}, 200
    except KeyError:
        response = {}, 404

    return response


def update_pet(pet_id, Pet):  # noqa: E501
    """Update and replace a pet in the store

     # noqa: E501

    :param pet_id: The id of the pet to update from the store
    :type pet_id: str
    :param Pet:
    :type Pet: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        Pet = Pet.from_dict(connexion.request.get_json())  # noqa: E501

    try:
        pets.update_pet(pet_id, Pet)
        response = {}, 200
    except KeyError:
        response = {}, 404

    return response'''