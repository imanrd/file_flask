import os
import io
from api import key, app
import logging
import pandas as pd
from flasgger import Swagger
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from flask import request, send_from_directory, abort, jsonify, Response

Swagger(app)

UPLOAD_FOLDER = './data/'
ALLOWED_EXTENSIONS = {'csv'}
UPLOADS_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOADS_PATH

app.secret_key = key.secret_key
app.config['SESSION_TYPE'] = 'filesystem'


def log_creator(name, file_name, level=logging.DEBUG):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    fh = logging.FileHandler(f"{file_name}.log")

    fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(fmt)
    fh.setFormatter(formatter)

    logger.addHandler(fh)
    return logger


logger = log_creator("code_info", "code_log")


def non_empty_string(s):
    if not s:
        raise ValueError("Must not be empty string")
    return s


@app.route('/file/<name>', methods=['Post'])
def post_file(name):
    """
    Upload a file
    This is using docstrings for specifications.
    ---
    parameters:
      - name: name
        in: path
        type: string
        required: true
    definitions:
      Name:
        type: file
        properties:
          palette_name:
            type: file
      Name:
        type: string
    responses:
      200:
        description: File is uploaded
        """
    logger.info(f"Upload '{name}' file")
    if "/" in name:
        abort(400, "no subdirectories allowed")
    if name != '':
        with open(os.path.join(UPLOAD_FOLDER, name), "wb") as fp:
            fp.write(request.data)
        response = {}, 201
    else:
        logger.warning("Error in upload!")
        response = {}, 400
    return response


@app.route('/file/<name>', methods=['Get'])
def get_file(name=None):
    """
    Download a file
    This is using docstrings for specifications.
    ---
    parameters:
      - name: name
        in: path
        type: string
        required: true
    definitions:
      Name:
        type: file
        properties:
          palette_name:
            type: file
      Name:
        type: string
    responses:
      200:
        description: File is downloaded
    """
    logger.info(f"Download '{name}' file")
    path = os.path.join(app.config['UPLOAD_FOLDER'], name)
    if os.path.exists(path):
        try:
            return send_from_directory(app.config["UPLOAD_FOLDER"], name)
        except Exception as ex:
            print(ex)
            logger.exception("Error in download!")
            return {}, 500
    else:
        return {}, 404


@app.route('/file/<name>', methods=['Delete'])
def delete_file(name):
    """
    Delete a file
    This is using docstrings for specifications.
    ---
    parameters:
      - name: name
        in: path
        type: string
        required: true
    definitions:
      Name:
        type: file
        properties:
          palette_name:
            type: file
      Name:
        type: string
    responses:
      200:
        description: File is deleted
    """
    logger.info(f"Delete '{name}' file")
    try:
        path = os.path.join(app.config['UPLOAD_FOLDER'], name)
        if os.path.exists(path):
            os.remove(path)
            response = {}, 200
        else:
            response = {}, 404
    except Exception as ex:
        print(ex)
        logger.exception("Error in delete!")
        response = {}, 500
    return response


@app.route('/list', methods=['Get'])
def list_file():
    """
    List directories files
    This is using docstrings for specifications.
    ---
    responses:
      200:
        description: List of files
    """
    list_of_files, dic_of_files = [], {}
    counter = 0
    for (_, _, filenames) in os.walk('./data'):
        list_of_files.extend(filenames)
    for item in list_of_files:
        counter += 1
        dic_of_files.update({counter: item})

    logger.info("List Files")
    return jsonify(dic_of_files)


@app.route('/draw/<name>/<x>/<y>', methods=['Get'])
def draw(name, x, y):
    """
    Draw diagram of two columns in a file
    This is using docstrings for specifications.
    ---
    parameters:
      - name: name
        in: path
        type: string
        required: true
      - name: x
        in: path
        type: string
        required: true
      - name: y
        in: path
        type: string
        required: true
    definitions:
      name:
        type: file
      x:
        type: string
      y:
        type: string
    responses:
      200:
        description: Draw diagram
        """
    kline = pd.read_csv(f"data/{name}")
    try:
        X = kline[x][-10:].tolist()
        Y = kline[y][-10:].tolist()
    except KeyError:
        return {}, 404
    X = [x[5:12] for x in X]
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.plot(X, Y)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


if __name__ == '__main__':
    logger.info("System Started!")
    app.run(debug=True)
