from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
import requests, jwt, json
from flask import session
salt = "อิอิอุอิ"

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=2, max=20)])
    confirm_password = PasswordField('Comfirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit')

    def validate_name(self, name):
        user = Users.objects(name = name.data).first()
        if user:
            raise ValidationError('That name is taken. Please Choose a different.')
    def validate_email(self, email):
        user = Users.objects(email = email.data).first()
        if user:
            raise ValidationError('That email is taken. Please Choose a different.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class GroupOfCamerasForm(FlaskForm):
    owner = StringField('Owner', validators=[DataRequired()])
    group_name = StringField('Group name', validators=[DataRequired(), Length(min=2, max=12)])    
    # c_lat = StringField('Lat', validators=[DataRequired(), Length(min=2, max=20)])
    # c_long = StringField('Long', validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Add')

    def validate_group_name(self, group_name):
        data = {
            "group_name":group_name.data,
            'access_token': session['google_token'],    
        }
        groups =jwt.encode( data,  salt, algorithm='HS256', headers={'message': 'OK'})
        r = requests.get("http://127.0.0.1:7000/api/group", data={'data':groups.decode('utf8')})
        r_data = json.loads(r.text)['test'].encode('utf8')
        groups = jwt.decode(r_data, salt, algorithms=['HS256'])
        print(group_name.data)
        # group = GroupOfCameras.objects(group_name = group_name.data).first()
        if not "error" in groups:
            raise ValidationError('That group_name is taken. Please Choose a different.')

    
class CamerasForm(FlaskForm):
    owner = StringField('Owner', validators=[DataRequired(), Length(min=1, max=50)])
    group_name = StringField('Group name', validators=[DataRequired(), Length(min=1, max=12)])
    name = StringField('Name of camera', validators=[DataRequired(), Length(min=1, max=12)])
    description = StringField('Description', validators=[Length(min=0, max=30)])
    uri = StringField('URI', validators=[DataRequired(), Length(min=2, max=200)])
    refresh = RadioField('Update Frame', choices=[('yes', 'Yes'), ('no', 'No')], validators=[DataRequired()])
    # port = StringField('Port', validators=[DataRequired(), Length(min=2, max=12)])
    # username = StringField('Username', validators=[DataRequired(), Length(min=2, max=12)])
    # password = PasswordField('Password', validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Confirm')