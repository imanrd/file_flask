import os
from flask import Flask, request, redirect, url_for, send_from_directory, render_template, abort, jsonify
from werkzeug.utils import secure_filename
from flask_restful import Api, Resource

from flasgger import Swagger
from flasgger.utils import swag_from
from flask_restful_swagger import swagger

import key

app = Flask(__name__)

UPLOAD_FOLDER = './data/'
ALLOWED_EXTENSIONS = {'csv'}
UPLOADS_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOADS_PATH

app.secret_key = key.secret_key
app.config['SESSION_TYPE'] = 'filesystem'

api = swagger.docs(Api(app), apiVersion='1', api_spec_url='/doc')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/flash')
def index():
    return render_template('index.html')


class FileTasks(Resource):

    @swagger.model
    @swagger.operation(notes="Upload a file")
    def post(self, name):

        if "/" in name:
            # Return 400 BAD REQUEST
            abort(400, "no subdirectories allowed")

        with open(os.path.join(UPLOAD_FOLDER, name), "wb") as fp:
            fp.write(request.data)

        # Return 201 CREATED
        return {}, 201

    @swagger.model
    @swagger.operation(notes="download a file")
    def get(self, name):
        path = os.path.join(app.config['UPLOAD_FOLDER'], name)
        if os.path.exists(path):
            try:
                return send_from_directory(app.config["UPLOAD_FOLDER"], name)
            except Exception as e:
                print(e)
                return {}, 500
        else:
            return {}, 404

    @swagger.model
    @swagger.operation(notes="Delete a file")
    def delete(self, name):
        path = os.path.join(app.config['UPLOAD_FOLDER'], name)
        if os.path.exists(path):
            os.remove(path)
            response = {}, 200
        else:
            response = {}, 404
        return response


class ListFiles(Resource):

    @swagger.model
    @swagger.operation(notes="List Files")
    def get(self):
        list_of_files, dic_of_files = [], {}
        counter = 0
        for (_, _, filenames) in os.walk('./data'):
            list_of_files.extend(filenames)
        # response_list = '\n'.join(list_of_files)
        # return jsonify(render_template('list.html', messages=list_of_files))
        for item in list_of_files:
            counter += 1
            dic_of_files.update({counter: item})

        return jsonify(dic_of_files)


api.add_resource(FileTasks, '/file/<string:name>', methods=['GET', 'POST', 'DELETE'])
api.add_resource(ListFiles, '/list')

if __name__ == '__main__':
    app.run(debug=True)
