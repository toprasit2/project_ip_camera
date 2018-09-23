from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from camera.models import Users, Cameras,GroupOfCameras
from flask import requests
# class RegistrationForm(FlaskForm):
#     name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
#     email = StringField('Email', validators=[DataRequired(), Email()])
#     password = PasswordField('Password', validators=[DataRequired(), Length(min=2, max=20)])
#     confirm_password = PasswordField('Comfirm Password', validators=[DataRequired(), EqualTo('password')])
#     submit = SubmitField('Submit')

#     def validate_name(self, name):
#         user = Users.objects(name = name.data).first()
#         if user:
#             raise ValidationError('That name is taken. Please Choose a different.')
#     def validate_email(self, email):
#         user = Users.objects(email = email.data).first()
#         if user:
#             raise ValidationError('That email is taken. Please Choose a different.')


# class LoginForm(FlaskForm):
#     email = StringField('Email', validators=[DataRequired(), Email()])
#     password = PasswordField('Password', validators=[DataRequired()])
#     remember = BooleanField('Remember Me')
#     submit = SubmitField('Login')

class GroupOfCamerasForm(FlaskForm):
    owner = StringField('Owner', validators=[DataRequired(), Length(min=2, max=20)])
    group_name = StringField('Group name', validators=[DataRequired(), Length(min=2, max=12)])
    submit = SubmitField('Add')

    def validate_group_name(self, group_name):
        group = GroupOfCameras.objects(group_name = group_name.data).first()
        if group:
            raise ValidationError('That group_name is taken. Please Choose a different.')

    
class CamerasForm(FlaskForm):
    owner = StringField('Owner', validators=[DataRequired(), Length(min=2, max=20)])
    group_name = StringField('Group name', validators=[DataRequired(), Length(min=2, max=12)])
    name = StringField('Name of camera', validators=[DataRequired(), Length(min=2, max=12)])
    uri = StringField('URI', validators=[DataRequired(), Length(min=2, max=20)])
    port = StringField('Port', validators=[DataRequired(), Length(min=2, max=12)])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=12)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Add Camera')