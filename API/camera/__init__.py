from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_mongoengine import MongoEngine
import jwt
app = Flask(__name__)
api = Api(app, prefix="/api")

app.config['MONGODB_SETTINGS'] = {
    'db' : 'admin',
    'host' : '127.0.0.1',
    'port' : 2277,
    'username':'admin',
    'password':'secure'
}
app.config['SECRET_KEY'] = '39380a3952f0ae125a699fd873560c51'
db = MongoEngine(app)

from camera.models import Users, GroupOfCameras, Cameras

salt = 'อิอิอุอิ'

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
        users = Users.objects(email=data['email']).first()
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
        users = Users.objects(email=data['email']).first()
        if not users:
            user_add = Users(
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
    def post(self):
        p = request.form['data']
        data = p.encode('utf8')
        data = jwt.decode(data, salt, algorithms=['HS256'])
        group_name = data['group_name']
        cameras = Cameras(
                group_name = group_name,
                owner = data['owner'],
                name = data['name'], 
                uri = data['uri'], 
                port = data['port'], 
                password = data['group_name'], 
                username = data['username']
        )
        cameras.save()
        encoded_jwt = jwt.encode( data,  salt, algorithm='HS256', headers={'message': 'OK'})
        return {"test": encoded_jwt.decode("utf-8")}

class CAMERAS(Resource):
    def get(self):
        p = request.form['data']
        data = p.encode('utf8')
        data = jwt.decode(data, salt, algorithms=['HS256'])
        encoded_jwt = jwt.encode( data,  salt, algorithm='HS256', headers={'message': 'OK'})
        cameras = Cameras.objects(owner = data['email'])
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
                        "port" : camera.port, 
                        "password" : camera.password, 
                        "username" : camera.username
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
        cameras = Cameras.objects(owner = data['email'], group_name=group_name)
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
        if 'group_id' in data:
            group = GroupOfCameras.objects.get(id=data['group_id'])
        else:
            group = GroupOfCameras.objects(group_name=data['group_name']).first()
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
                c_lat = data['c_lat'],
                c_long = data['c_long']
        )
        group.save()
        encoded_jwt = jwt.encode( data,  salt, algorithm='HS256', headers={'message': 'OK'})
        return {"test": encoded_jwt.decode("utf-8")}

class GROUPS(Resource):
    def get(self):
        p = request.form['data']
        data = p.encode('utf8')
        data = jwt.decode(data, salt, algorithms=['HS256'])
        groups = GroupOfCameras.objects(owner=data['email'])
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