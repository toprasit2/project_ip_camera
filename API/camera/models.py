from flask_login import UserMixin
from flask_mongoengine.wtf import model_form
from camera import db
# , login_manager
from datetime import datetime

# @login_manager.user_loader
# def load_user(user_id):
#     return Users.objects.get(id=user_id)
class SharedCameras(db.Document):
    camera_id = db.StringField(max_length = 50)
    shared = db.StringField(max_length = 50)

class MyUsers(db.Document, UserMixin):
    name = db.StringField(max_length = 20)
    email = db.EmailField(max_length = 50)
    picture = db.StringField()
    permission = db.StringField(default='user')
    access_date = db.DateTimeField(default=datetime.utcnow)
    
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
    uri = db.StringField(max_length = 200)
    refresh = db.StringField(max_length = 10)
    # port = db.StringField(max_length = 50)
    # username = db.StringField(max_length = 50)
    # password = db.StringField(max_length = 50)
    create_date = db.DateTimeField(default=datetime.utcnow)
    compute_id = db.StringField(max_length = 50,default="None")
    shared = db.StringField(max_length = 50)

class CPUUsage(db.EmbeddedDocument):
    used = db.FloatField(default=0)  # show in percent
    used_per_cpu = db.ListField(db.FloatField())

class MemoryUsage(db.EmbeddedDocument):
    used = db.IntField(default=0)
    free = db.IntField(default=0)
    total = db.IntField(required=True, default=0)

class DiskUsage(db.EmbeddedDocument):
    used = db.IntField(default=0)
    free = db.IntField(default=0)
    percent = db.FloatField(default=0)  # show in percent
    total = db.IntField(required=True, default=0)

class ComputeNodes(db.Document):
    name = db.StringField(max_length = 50)
    owner = db.StringField(max_length = 50)
    cpu = db.EmbeddedDocumentField(
        'CPUUsage', required=True, default=CPUUsage())
    memory = db.EmbeddedDocumentField(
        'MemoryUsage', required=True, default=MemoryUsage())
    disk = db.EmbeddedDocumentField(
        'DiskUsage', required=True, default=DiskUsage())
    create_date = db.DateTimeField(default=datetime.utcnow)
    online = db.StringField(max_length = 50)

class CameraInComputeNodes(db.Document):
    camera_name = db.StringField(max_length = 50)
    compute_name = db.StringField(max_length = 50)
    owner = db.StringField(max_length = 50)

class PermissionList(db.Document):
    permission = db.StringField(max_length = 20)