from flask import Flask, render_template, request
from mainfun import *
import os
# from flask_wtf import FlaskForm
# from wtforms import FileField, SubmitField
# from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/')
def Index():
    return render_template("index.html")

@app.route('/predict', methods=['POST'])
def predict():
    # if 'file' in request.files:
    f = request.files['file']
    basepath = os.path.dirname(__file__)
    filepath = os.path.join(basepath, 'static\\files', f.filename)
    # print("upload folder is", filepath)
    f.save(filepath)
    fun()
    return render_template("predict.html")