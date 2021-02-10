from application import db
import datetime as dt

from sqlalchemy.orm import validates

class Entry(db.Model):
    __tablename__ = 'predictions'
 
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    image_name = db.Column(db.String(50))
    prediction = db.Column(db.String(10))
    username = db.Column(db.String)
    predicted_on = db.Column(db.DateTime, nullable=False)
    @validates('image_name') 
    def validate_username(self, key, username):
        if len('image_name')>50:
            raise AssertionError('Value must smaller than 50')
        return image_name
    @validates('prediction') 
    def validate_password(self, key, password):
        if len('prediction')>10:
            raise AssertionError('Value must smaller than 50')
        return prediction
    @validates('username') 
    def validate_password(self, key, password):
        if len('username')>50:
            raise AssertionError('Value must smaller than 50')
        return username



class Accounts(db.Model):
    __tablename__ = 'Accounts'
 
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    created_on = db.Column(db.DateTime, nullable=False)
    @validates('username') 
    def validate_username(self, key, username):
        if len('username')>50:
            raise AssertionError('Value must smaller than 50')
        return username
    @validates('password') 
    def validate_password(self, key, password):
        if len('password')>50:
            raise AssertionError('Value must smaller than 50')
        return password
