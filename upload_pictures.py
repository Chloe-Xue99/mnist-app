
# coding:utf-8
import os
import flask
import io
import datetime
import time
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename

import tensorflow as tf
import numpy as np
from PIL import Image
import train
import predict
import connect

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp'])

CKPT_DIR = 'model'


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/images/'


def parse(name, time):
    temp = []
    temp.append(str(time))
    temp.append('_')
    temp.append(name)
    name = ''.join(temp)
    return name


# @app.route('/upload', methods=['POST', 'GET'])
@app.route('/upload', methods=['POST', 'GET'])
def upload():
    req_time = datetime.datetime.now()
    if request.method == 'POST':
        f = request.files['file']
        upload_filename = secure_filename((f).filename)

        if not (f and allowed_file(f.filename)):
            return jsonify({"error": 1001, "msg": "Types of files only limited to png, PNG, jpg, JPG, bmp"})

        save_filename = parse(upload_filename, req_time)
        save_filepath = os.path.join(
            app.root_path, app.config['UPLOAD_FOLDER'], save_filename)
        f.save(save_filepath)
        mnist_result = (predict.predict(save_filepath))

        user_input = request.form.get("name")

        basepath = os.path.dirname(__file__)

        # upload_path = os.path.join(
        # basepath, 'static/images', secure_filename(f.filename))
        # upload_path = os.path.join(basepath, 'static/images','test.jpg')
        f.save(save_filepath)

        mnist_result = str(predict(save_filepath))
        connect.insertData(request.remote_addr, req_time,
                           save_filepath, mnist_result)

        # img = cv2.imread(upload_path)
        # cv2.imwrite(os.path.join(basepath, 'static/images', 'test.jpg'), img)
        # result1 = main(resize(upload_path))
        result1 = "%s%s%s%s%s%s%s%s%s" % ("Upload File Name: ", upload_filename, "\n",
                                          "Upload Time: ", req_time, "\n",
                                          "Prediction: ", mnist_result, "\n")

        return render_template('upload_ok.html', userinput=user_input, val1=time.time(), result=result1)

    return render_template('upload.html')

# Go to '127.0.0.1:8987/upload' on the server computer


if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    # app.debug = True
    # app.run(debug=True, use_reloader=False, host='0.0.0.0')
    app.run(debug=True, use_reloader=False, port=8987, host='0.0.0.0')
