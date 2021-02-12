from application import app, db
from flask import render_template, request, flash
from flask_cors import CORS, cross_origin
from flask import json, jsonify
from flask import abort, redirect, url_for, session
from sqlalchemy.orm.exc import UnmappedInstanceError
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
import pytz

#create the database if not exist
db.create_all()

#labels for prediction
labels = ['Angry','Fear','Sad','Neutral','Happy', 'Surprise']

timezone = pytz.timezone("Etc/GMT+8")

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
    except UnmappedInstanceError:
        pass
    except Exception as error:
        db.session.rollback()
        flash(error,"danger")


def get_entry(id):
    try:
        entries = Entry.query.filter(Entry.id==id)
        result = entries[0]
        return result
    except Exception as error:
        db.session.rollback()
        flash(error,"danger") 
        return 0  


def parseImage(imgData):
    # parse canvas bytes and save as output.png
    imgstr = re.search(b'base64,(.*)', imgData).group(1)
    filename = './static/images/output-{}.png'.format(datetime.now())
    with open(filename,'wb') as output:
        output.write(base64.decodebytes(imgstr))
    return filename
 
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
    if 'username' not in session and (request.endpoint != 'login' and request.endpoint != 'register') and request.endpoint not in ['api_add','api_get','api_delete','api_getall','api_predict']:
        return redirect(url_for('login'))


#Handles http://127.0.0.1:5000/
@app.route('/') 
@app.route('/index') 
@app.route('/home') 
def index_page(): 
    return render_template('index.html')
 
#Handles http://127.0.0.1:5000/predict
@app.route("/predict", methods=['GET', 'POST'])
@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
def predict():
    # get data from drawing canvas and save as image
    filename = parseImage(request.get_data())

    # Decoding and pre-processing base64 image
    img = image.img_to_array(image.load_img(filename, color_mode="grayscale", target_size=(48, 48))) / 255.

    # reshape data to have a single channel
    img = img.reshape(1,48,48,1)

    predictions = make_prediction(img)
    
    for i, pred in enumerate(predictions):
        label_pred = "{}".format(labels[np.argmax(pred)])
    

    new_entry = Entry(image_name=timezone.localize(datetime.now()).strftime("%d %B %Y, ")+ label_pred+ " by " + session['username'],
                        prediction=label_pred,
                        username=session['username'],
                        predicted_on=timezone.localize(datetime.now()))
    add_entry(new_entry)

    response = []
    for i in predictions[0]:
        response.append(i)

    ret = ""
    for i, pred in enumerate(predictions):
        ret = "{}".format(labels[np.argmax(pred)])
    response.append(ret)
    return jsonify(response)
        
@app.route('/view') 
def view_page():
        entries = get_entries(session['username'])
        return render_template("view.html",title="View past results", entries = entries)

@app.route('/remove', methods=['POST'])
def remove():
    req = request.form
    id = req["id"]
    remove_entry(id)
    return redirect(url_for('view_page'))


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
                            created_on=timezone.localize(datetime.now()))
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

# test apis

@app.route("/api/add", methods=['POST'])
def api_add(): 

    data = request.get_json()

    image_name        = data['image_name']
    prediction        = data['prediction']
    username          = data['username']

    new_entry = Entry(image_name=image_name,
                        prediction=prediction,
                        username=username,
                        predicted_on=timezone.localize(datetime.now()))

    #invoke the add entry function to add entry                        
    result = add_entry(new_entry)
    #return the result of the db action
    return jsonify({'id':result})

@app.route("/api/get/<id>", methods=['GET'])
def api_get(id): 
    #retrieve the entry using id from client
    entry = get_entry(int(id))
    #Prepare a dictionary for json conversion
    data = {   'id' : entry.id,
                'image_name':entry.image_name,
                'prediction':entry.prediction,
                'username':entry.username,
                'predicted_on' : entry.predicted_on }
#Convert the data to json
    result = jsonify(data)
    return result #response back

#API delete entry
@app.route("/api/delete/<id>", methods=['GET'])
def api_delete(id): 
    entry = remove_entry(int(id))
    return jsonify({'result':'ok'})

@app.route("/api/getall/<name>", methods=['GET'])
def api_getall(name): 
    entry = get_entries(str(name))
    return jsonify({'result':'ok'})

@app.route("/api/predict", methods=['POST'])
def api_predict(): 
    filename = parseImage(request.get_data())
    img = image.img_to_array(image.load_img(filename, color_mode="grayscale", target_size=(48, 48))) / 255.
    img = img.reshape(1,48,48,1)
    predictions = make_prediction(img)
    for i, pred in enumerate(predictions):
        ret = "{}".format(labels[np.argmax(pred)])
    return jsonify({'result':'ok', 'result': ret, 'probability': predictions[0]})


    