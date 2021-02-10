from application import app, db
from flask import render_template, request, flash
from flask_cors import CORS, cross_origin
from flask import json, jsonify
from flask import abort, redirect, url_for, session
from application.forms import LoginForm, RegisterForm
from keras.preprocessing import image
from PIL import Image, ImageOps
import numpy as np
import keras.models
import re
import base64
from io import BytesIO
import json
import numpy as np
import requests
import pathlib, os
import tempfile
from application.models import Entry, Accounts
from datetime import datetime

#create the database if not exist
db.create_all()

#labels for prediction
labels = ['Angry','Fear','Happy','Sad','Surprise', 'Neutral']

def get_user(username):
    try:
        entries = Accounts.query.filter_by(username=username).first()
        result = entries
        if result is None:
            return False
        return result
    except Exception as error:
        db.session.rollback()
        return 0  

def add_entry(new_entry):
    try:
        db.session.add(new_entry)
        db.session.commit()
        return new_entry.id
 
    except Exception as error:
        db.session.rollback()
        flash(error,"danger")

def get_entries(username):
        try:
            entries = Entry.query.filter(Entry.username == username).all()
            if entries == 0:
                return []
            return entries
        except Exception as error:
            db.session.rollback()
            flash(error,"danger") 
            return 0


def remove_entry(id):
    try:
        entry = Entry.query.get(id)
        db.session.delete(entry)
        db.session.commit()
    except Exception as error:
        db.session.rollback()
        flash(error,"danger")


def parseImage(imgData):
    # parse canvas bytes and save as output.png
    imgstr = re.search(b'base64,(.*)', imgData).group(1)
    with tempfile.TemporaryDirectory() as tmpdirname:
        with open(tmpdirname + 'output.png','wb') as output:
            output.write(base64.decodebytes(imgStr))
 
def make_prediction(instances):
    data = json.dumps({"signature_name": "serving_default", "instances": instances.tolist()})
    headers = {"content-type": "application/json"}
    json_response = requests.post(url, data=data, headers=headers)
    predictions = json.loads(json_response.text)['predictions']
    return predictions
 
#server URL
url = 'https://ca2-2b11-asdfasdf-tf.herokuapp.com/v1/models/img_classifier:predict'
 
@app.before_request
def before_request():
    if 'username' not in session and (request.endpoint != 'login' and request.endpoint != 'register'):
        return redirect(url_for('login'))


#Handles http://127.0.0.1:5000/
@app.route('/') 
@app.route('/index') 
@app.route('/home') 
def index_page(): 
    return render_template('index.html')
 
#Handles http://127.0.0.1:5000/predict
@app.route("/predict", methods=['POST'])
@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
def predict():
    if request.method == 'POST':
        # get data from drawing canvas and save as image
        parseImage(request.get_data())
        print("bruh")
        # Build directory
        img_dir = tempfile.TemporaryDirectory() + "output.png"
        print(img_dir)
        # Decoding and pre-processing base64 image
        img = image.img_to_array(image.load_img(img_dir, color_mode="grayscale", target_size=(48, 48)) / 255.)
        # reshape data to have a single channel
        img = img.reshape(1,48,48,1)
    
        predictions = make_prediction(img)
        
        new_entry = Entry(  image_name=datetime.now().strftime("%d %B %Y") + session['username'],
                            prediction=labels[np.argmax(predictions)],
                            username=session['username'],
                            predicted_on=datetime.utcnow())
        add_entry(new_entry)


        ret = ""
        for i, pred in enumerate(predictions):
            ret = "{}".format(labels[np.argmax(pred)])
            response = ret
            return response
        
@app.route('/view') 
def view_page():
        entries = get_entries(session['username'])
        return render_template("view.html",title="View past results", entries = entries)



@app.route('/remove', methods=['POST'])
def remove():
    form = PredictionForm()
    req = request.form
    id = req["id"]
    remove_entry(id)
    return redirect(url_for('index_page'))


@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if 'username' in session:
        session.pop('username', None)
        flash("You have been logged out of your previous session")
    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            password_check = get_user(username)
            if (password_check == 0):
                flash("Username not found", "danger")
            elif (password == password_check.password):
                session['username'] = username
                return redirect(url_for('index_page'))
            else:
                flash("Password is incorrect", "danger")
        else:
            flash("Error, cannot proceed with login","danger")
    return render_template("login.html", form=form, title="Login")

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            unique_check = get_user(username)
            if unique_check == 0:
                new_entry = Accounts(  
                            username=username, password=password,
                            created_on=datetime.utcnow())
                add_entry(new_entry)
                return redirect(url_for('login'))
            else:
                flash("Username is already taken", "danger")
        else:
            flash("Error, cannot proceed with register","danger")
    return render_template("register.html", form=form, title="Register")
    
@app.route('/logout', methods=['GET'])
def logout():
    if 'username' in session:
        session.pop('username', None)
    return redirect(url_for('login'))



    