from flask_login import UserMixin
from flask_mongoengine.wtf import model_form
from camera import db
# , login_manager
from datetime import datetime

# @login_manager.user_loader
# def load_user(user_id):
#     return Users.objects.get(id=user_id)

class Users(db.Document, UserMixin):
    name = db.StringField(max_length = 20)
    email = db.EmailField(max_length = 50)
    picture = db.StringField()
    permission = db.StringField(default='user')
    def __repr__(self):
        return f"User('{self.name}', '{self.email}'')"

class GroupOfCameras(db.Document):
    group_name = db.StringField(max_length = 50)
    owner = db.StringField(max_length = 50)
    create_date = db.DateTimeField(default=datetime.utcnow)
    c_lat = db.StringField(max_length = 50)
    c_long = db.StringField(max_length = 50)

class Cameras(db.Document):
    owner = db.StringField(max_length = 50)
    group_name = db.StringField(max_length = 50)
    name = db.StringField(max_length = 12)
    description = db.StringField(max_length = 50)
    uri = db.StringField(max_length = 50)
    port = db.StringField(max_length = 50)
    username = db.StringField(max_length = 50)
    password = db.StringField(max_length = 50)
    create_date = db.DateTimeField(default=datetime.utcnow)