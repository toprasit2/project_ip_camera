from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_mongoengine import MongoEngine
import jwt
import httplib2
import json
app = Flask(__name__)
api = Api(app, prefix="/api")

app.config['MONGODB_SETTINGS'] = {
    'db' : 'admin',
    'host' : '127.0.0.1',
    'port' : 1122,
    'username':'',
    'password':''
}
app.config['SECRET_KEY'] = '39380a3952f0ae125a699fd873560c51'
db = MongoEngine(app)

from google.oauth2 import id_token
from google.auth.transport import requests


from camera.models import MyUsers, GroupOfCameras, Cameras

salt = 'อิอิอุอิ'

def check_token(access_token):
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'% access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1].decode('utf-8'))
    return result

class MY_NAME(Resource):
    def get(self):
        data = {'username': ['Thanaphon Toprasit','GENG']}
        encoded_jwt = jwt.encode( data,  salt, algorithm='HS256', headers={'message': 'OK'})
        return {"test": encoded_jwt.decode("utf-8")}
    def put(self):
        p = request.form['data']
        name = p.encode('utf8')
        d_name = jwt.decode(name, salt, algorithms=['HS256'])
        data = {
            'name': d_name['name']
        }
        encoded_jwt = jwt.encode( data,  salt, algorithm='HS256', headers={'message': 'OK'})
        return {"test": encoded_jwt.decode("utf-8")}

class USER(Resource):
    def get(self):
        p = request.form['data']
        data = p.encode('utf8')
        data = jwt.decode(data, salt, algorithms=['HS256'])
        users = MyUsers.objects(email=data['email']).first()
        if users:
            data = {
                'id': str(users.id),
                'name' : users.name,
                'email' : users.email,
                'picture' : users.picture,
                'permission' : users.permission
            }
        encoded_jwt = jwt.encode( data,  salt, algorithm='HS256', headers={'message': 'OK'})
        return {"test": encoded_jwt.decode("utf-8")}
    def post(self):
        p = request.form['data']
        data = p.encode('utf8')
        data = jwt.decode(data, salt, algorithms=['HS256'])
        users = MyUsers.objects(email=data['email']).first()
        if not users:
            user_add = MyUsers(
                name=data['name'],
                email=data['email'],
                picture=data['picture']
            )
            user_add.save()
            if user_add:
                return{'status':"200"}
            else:
                return{'status':"404"}
        return{'status':"200"}

class CAMERA(Resource):
    def get(self):
        p = request.form['data']
        data = p.encode('utf8')
        data = jwt.decode(data, salt, algorithms=['HS256'])
        encoded_jwt = jwt.encode( data,  salt, algorithm='HS256', headers={'message': 'OK'})
        cameras = Cameras.objects(id = data['camera_id'])
        data= []
        for camera in cameras:
            data.append(
                { 
                    "id" : str(camera.id),
                    "group_name" : camera.group_name,
                    "owner" : camera.owner,
                    "name" : camera.name,
                    "description" : camera.description,
                    "uri" : camera.uri,
                    "refresh": camera.refresh
                }
            )
        data = {
            "data":data
        }
        encoded_jwt = jwt.encode( data,  salt, algorithm='HS256', headers={'message': 'OK'})
        return {"test": encoded_jwt.decode("utf-8")}
    def post(self):
        p = request.form['data']
        data = p.encode('utf8')
        data = jwt.decode(data, salt, algorithms=['HS256'])
        group_name = data['group_name']
        cameras = Cameras(
                group_name = group_name,
                owner = data['owner'],
                description = data['description'],
                name = data['name'], 
                uri = data['uri'],
                refresh = data['refresh']
        )
        cameras.save()
        encoded_jwt = jwt.encode( data,  salt, algorithm='HS256', headers={'message': 'OK'})
        return {"test": encoded_jwt.decode("utf-8")}
    def delete(self):
        p = request.form['data']
        data = p.encode('utf8')
        data = jwt.decode(data, salt, algorithms=['HS256'])
        camera_id = data['camera_id']
        cameras = Cameras.objects(id = camera_id)
        cameras.delete()
        encoded_jwt = jwt.encode( data,  salt, algorithm='HS256', headers={'message': 'OK'})
        return {"test": encoded_jwt.decode("utf-8")}
    def put(self):
        p = request.form['data']
        data = p.encode('utf8')
        data = jwt.decode(data, salt, algorithms=['HS256'])
        camera = Cameras.objects(id = data['camera_id'])
        print(camera)
        camera.update(set__group_name=data['group_name'])
        camera.update(set__owner=data['owner'])
        camera.update(set__description=data['description'])
        camera.update(set__name=data['name'])
        camera.update(set__uri=data['uri'])
        camera.update(set__refresh=data['refresh'])
        # if camera:
        #     camera['group_name'] = data['group_name']
        #     camera['owner'] = data['owner']
        #     camera['description'] = data['description']
        #     camera['name'] = data['name']
        #     camera['uri'] = data['uri']
        #     camera['refresh'] = data['refresh']
        #     camera.save()
        #     print('save')
        #     if camera:
        #         return{'status':"200"}
        #     else:
        #         return{'status':"404"}
        return{'status':"200"}

class CAMERAS(Resource):
    def get(self):
        p = request.form['data']
        data = p.encode('utf8')
        data = jwt.decode(data, salt, algorithms=['HS256'])
        encoded_jwt = jwt.encode( data,  salt, algorithm='HS256', headers={'message': 'OK'})
        access_token = data['access_token'][0]
        user = check_token(access_token)
        cameras = Cameras.objects(owner = user['email'])
        data= []
        if cameras != None:
            for camera in cameras:
                data.append(
                    { 
                        "id" : str(camera.id),
                        "group_name" : camera.group_name,
                        "owner" : camera.owner,
                        "name" : camera.name,
                        "description" : camera.description,
                        "uri" : camera.uri,
                        "refresh": camera.refresh
                    }
                )
            data = {
                "data":data
            }
        else:
            data = {
                'error':'error'
            }
        encoded_jwt = jwt.encode( data,  salt, algorithm='HS256', headers={'message': 'OK'})
        return {"test": encoded_jwt.decode("utf-8")}
    
class CAMERAS_IN_GROUP(Resource):
    def get(self):
        p = request.form['data']
        data = p.encode('utf8')
        data = jwt.decode(data, salt, algorithms=['HS256'])
        encoded_jwt = jwt.encode( data,  salt, algorithm='HS256', headers={'message': 'OK'}) 
        group = GroupOfCameras.objects.get(id=data['group_id'])
        group_name = group.group_name
        access_token = data['access_token'][0]
        user = check_token(access_token)
        cameras = Cameras.objects(owner = user['email'], group_name=group_name)
        data= []
        if cameras != None:
            for camera in cameras:
                data.append(
                    { 
                        "id":str(camera.id),
                        "group_name":camera.group_name,
                        "owner":camera.owner,
                        "name":camera.name,
                        "description":camera.description,
                        "uri":camera.uri, 
                        "port":camera.port, 
                        "password":camera.password, 
                        "username":camera.username
                    }
                )
            data = {
                "data":data
            }
        else:
            data = {
                'error':'error'
            }
        encoded_jwt = jwt.encode( data,  salt, algorithm='HS256', headers={'message': 'OK'})
        return {"test": encoded_jwt.decode("utf-8")}

class GROUP(Resource):
    def get(self):
        p = request.form['data']
        data = p.encode('utf8')
        data = jwt.decode(data, salt, algorithms=['HS256'])
        encoded_jwt = jwt.encode( data,  salt, algorithm='HS256', headers={'message': 'OK'})
        access_token = data['access_token'][0]
        user = check_token(access_token)
        if 'group_id' in data:
            group = GroupOfCameras.objects.get(id=data['group_id'])
        else:
            group = GroupOfCameras.objects(group_name=data['group_name'], owner=user['email']).first()
        if group != None:
            data = {
                "owner":group.owner,
                "group_name":group.group_name,
                "id":str(group.id)
            }
        else:
            data = {
                'error':'error'
            }
        encoded_jwt = jwt.encode( data,  salt, algorithm='HS256', headers={'message': 'OK'})
        return {"test": encoded_jwt.decode("utf-8")}
    def post(self):
        p = request.form['data']
        data = p.encode('utf8')
        data = jwt.decode(data, salt, algorithms=['HS256'])
        group_name = data['group_name']
        group = GroupOfCameras(
                group_name = data['group_name'],
                owner= data['owner'],
                # c_lat = data['c_lat'],
                # c_long = data['c_long']
        )
        group.save()
        encoded_jwt = jwt.encode( data,  salt, algorithm='HS256', headers={'message': 'OK'})
        return {"test": encoded_jwt.decode("utf-8")}
    def delete(self):
        p = request.form['data']
        data = p.encode('utf8')
        data = jwt.decode(data, salt, algorithms=['HS256'])
        group_id = data['group_id']
        group = GroupOfCameras.objects(id = group_id)
        group.delete()
        encoded_jwt = jwt.encode( data,  salt, algorithm='HS256', headers={'message': 'OK'})
        return {"test": encoded_jwt.decode("utf-8")}
    def put(self):
        p = request.form['data']
        data = p.encode('utf8')
        data = jwt.decode(data, salt, algorithms=['HS256'])
        access_token = data['access_token'][0]
        user = check_token(access_token)
        group = GroupOfCameras.objects(id = data['group_id'], owner=user['email']).first()
        print(group.group_name)
        cameras = Cameras.objects(owner=user['email'], group_name=group['group_name'])
        group.update(set__group_name=data['group_name'])
        print(cameras)
        for camera in cameras:
            camera.update(set__group_name=data['group_name'])
        return {'status':"200"}

class GROUPS(Resource):
    def get(self):
        p = request.form['data']
        data = p.encode('utf8')
        data = jwt.decode(data, salt, algorithms=['HS256'])
        access_token = data['access_token'][0]
        user = check_token(access_token)
        groups = GroupOfCameras.objects(owner=user['email'])
        data = []
        if groups:
            for group in groups:
                data.append(
                    {
                        'group_name':group.group_name,
                        'owner':group.owner,
                        'id' : str(group.id)
                    }
                )
            data = {
                "data":data
            }
        else:
            data = {
                'error':'error'
            }
        encoded_jwt = jwt.encode( data,  salt, algorithm='HS256', headers={'message': 'OK'})
        return {"test": encoded_jwt.decode("utf-8")}

class PROCESSER(Resource):
    def get(self):
        data = {
            "name": 'test',
            "value": 2016
        }
        return jsonify(data)

api.add_resource(MY_NAME, '/name')
api.add_resource(USER, '/user')
api.add_resource(CAMERA, '/camera')
api.add_resource(CAMERAS, '/cameras')
api.add_resource(CAMERAS_IN_GROUP, '/cameras_in_group')
api.add_resource(GROUP, '/group')
api.add_resource(GROUPS, '/groups')
api.add_resource(PROCESSER, '/processer')