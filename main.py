import os
import io
import key
import logging
import pandas as pd
from matplotlib.figure import Figure
from flask_restful import Api, Resource
from flask_restful_swagger import swagger
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from flask import Flask, request, send_from_directory, render_template, abort, jsonify, Response


app = Flask(__name__)

UPLOAD_FOLDER = './data/'
ALLOWED_EXTENSIONS = {'csv'}
UPLOADS_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOADS_PATH

app.secret_key = key.secret_key
app.config['SESSION_TYPE'] = 'filesystem'

api = swagger.docs(Api(app), apiVersion='1', api_spec_url='/doc')


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


class FileTasks(Resource):

    @swagger.model
    @swagger.operation(notes="Upload a file")
    def post(self, name):
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

    @swagger.model
    @swagger.operation(notes="download a file")
    def get(self, name=None):
        if not name:
            raise Exception("Name is required!")
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

    @swagger.model
    @swagger.operation(notes="Delete a file")
    def delete(self, name):
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


class ListFiles(Resource):

    @swagger.model
    @swagger.operation(notes="List Files")
    def get(self):
        list_of_files, dic_of_files = [], {}
        counter = 0
        for (_, _, filenames) in os.walk('./data'):
            list_of_files.extend(filenames)
        for item in list_of_files:
            counter += 1
            dic_of_files.update({counter: item})

        logger.info("List Files")
        return jsonify(dic_of_files)


class Diagram(Resource):

    @swagger.model
    @swagger.operation(notes="List Files")
    def get(self, name, xo, yc):
        kline = pd.read_csv(f"data/{name}")
        try:
            x = kline[xo][-10:].tolist()
            y = kline[yc][-10:].tolist()
        except KeyError:
            return {}, 404
        x = [x[5:12] for x in x]
        fig = Figure()
        axis = fig.add_subplot(1, 1, 1)
        axis.plot(x, y)
        output = io.BytesIO()
        FigureCanvas(fig).print_png(output)
        return Response(output.getvalue(), mimetype='image/png')


# There must be a way to handle empty file names
api.add_resource(FileTasks, '/file/<string:name>', methods=['GET', 'POST', 'DELETE'])

api.add_resource(ListFiles, '/list')

api.add_resource(Diagram, '/draw/<string:name>/<string:xo>/<string:yc>')

if __name__ == '__main__':
    logger.info("System Started!")
    app.run(debug=True)
