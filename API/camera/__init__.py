from flask import Flask, request, jsonify, Response
from flask_restful import Resource, Api
from flask_mongoengine import MongoEngine
import jwt
import httplib2
import json
import cv2
import urllib
import base64
import numpy as np
#processor data
from nokkhumclient import client
from datetime import datetime

import random
import string

app = Flask(__name__)
api = Api(app, prefix="/api")

app.config['MONGODB_SETTINGS'] = {
    'db' : 'admin',
    'host' : '127.0.0.1',
    'port' : 27017,
    'username':'',
    'password':''
}
app.config['SECRET_KEY'] = '39380a3952f0ae125a699fd873560c51'
db = MongoEngine(app)

from google.oauth2 import id_token
from google.auth.transport import requests


from camera.models import MyUsers, GroupOfCameras, Cameras,ComputeNodes, SharedCameras, PermissionList

salt = 'อิอิอุอิ'

def check_token(access_token):
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'% access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1].decode('utf-8'))
    return result

def nokkhum_client():        
        host = 'nvr.coe.psu.ac.th'
        port = 6543
        
        username = 'admin@nokkhum.local'
        password = 'password'
        
        secure_connection = False
        
        # token = session['google_token']
        # token = token[0]
        token = None
        nk_client = client.Client(username, 
                                  password, 
                                  host, 
                                  port, 
                                  secure_connection, 
                                  token)
        return nk_client

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
        users.update(set__last_access=datetime.now())
        if users:
            data = {
                'id': str(users.id),
                'name' : users.name,
                'email' : users.email,
                'picture' : users.picture,
                'permission' : users.permission,
                'last_access': str(users.last_access),
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
                    "refresh": camera.refresh,
                    "shared": camera.shared
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
        access_token = data['access_token'][0]
        user = check_token(access_token)
        camera = Cameras.objects(id = data['camera_id'], owner= user['email'])
        camera.update(set__group_name=data['group_name'])
        camera.update(set__owner=user['email'])
        camera.update(set__description=data['description'])
        camera.update(set__name=data['name'])
        camera.update(set__uri=data['uri'])
        camera.update(set__refresh=data['refresh'])
        camera.update(set__update_date=datetime.now())
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
                cid = str(camera.id)
                shared = SharedCameras.objects(camera_id = cid)
                t_shared = []
                for i in shared:
                    t_shared.append(i.shared)
                data.append(
                    { 
                        "id" : str(camera.id),
                        "group_name" : camera.group_name,
                        "owner" : camera.owner,
                        "name" : camera.name,
                        "description" : camera.description,
                        "uri" : camera.uri,
                        "refresh": camera.refresh,
                        "compute_id": camera.compute_id,
                        "shared" : t_shared
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
        group = GroupOfCameras.objects(id = group_id).first()
        cameras = Cameras.objects(group_name = group.group_name)
        for c in cameras:
            c.delete()
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

class PROCESSOR(Resource):
    def get(self):
        p = request.form['data']
        data = p.encode('utf8')
        data = jwt.decode(data, salt, algorithms=['HS256'])
        encoded_jwt = jwt.encode( data,  salt, algorithm='HS256', headers={'message': 'OK'})
        access_token = data['access_token'][0]
        user = check_token(access_token)
        if 'processor_id' in data:
            processor = ComputeNodes.objects(owner=user['email'], id=data['processor_id'])
        if processor != None:
            for p in processor:
                data = {
                    "name":p.name,
                    "id":str(p.id),
                    "key":p.key,
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
        id = data['id']
        lettersAndDigits = string.ascii_letters + string.digits
        key = ''.join(random.choice(lettersAndDigits) for i in range(10))
        compute = ComputeNodes.objects(id=id).first()
        compute.update(set__key=key)
        data = {
            "key":key,
            "id":id
        }
        encoded_jwt = jwt.encode( data,  salt, algorithm='HS256', headers={'message': 'OK'})
        return {"test": encoded_jwt.decode("utf-8")}
    def put(self):
        p = request.form['data']
        data = p.encode('utf8')
        data = jwt.decode(data, salt, algorithms=['HS256'])
        access_token = data['access_token'][0]
        user = check_token(access_token)
        compute = ComputeNodes.objects(id=data['id'], owner= user['email']).first()
        compute.update(set__name=data['name'])
        com_id = str(compute.id)
        cameras = Cameras.objects(owner=user['email'], compute_id=data['id'])
        for camera in cameras:
            camera.update(set__compute_id='None')
        for c_id in data['cameras']:
            camera = Cameras.objects(id=c_id).first()
            camera.update(set__compute_id=com_id)
            print(c_id)
        return {'status':"200"}
    def delete(self):
        p = request.form['data']
        data = p.encode('utf8')
        data = jwt.decode(data, salt, algorithms=['HS256'])
        access_token = data['access_token'][0]
        user = check_token(access_token)
        processor_id = data['processor_id']
        processor = ComputeNodes.objects(id = processor_id).first()
        cameras = Cameras.objects(owner=user['email'], compute_id=processor_id)
        for camera in cameras:
            camera.update(set__compute_id='None')
        processor.delete()
        encoded_jwt = jwt.encode( data,  salt, algorithm='HS256', headers={'message': 'OK'})
        return {"test": encoded_jwt.decode("utf-8")}

class PROCESSORS(Resource):
    def get(self):
        p = request.form['data']
        data = p.encode('utf8')
        data = jwt.decode(data, salt, algorithms=['HS256'])
        encoded_jwt = jwt.encode( data,  salt, algorithm='HS256', headers={'message': 'OK'})
        access_token = data['access_token'][0]
        if len(access_token) < 5:
            access_token = data['access_token']
        user = check_token(access_token)
        user = MyUsers.objects(email=user['email']).first()
        # if user['permission'] == 'admin':
        #     nk = nokkhum_client()
        #     processors = nk.admin.processors.list()
        #     compute_nodes = nk.admin.compute_nodes.list()
        #     nodes = []
        #     for c in compute_nodes:
        #         nodes.append(nk.admin.compute_nodes.get(c.id))
        #     ps = []
        #     for p in processors:
        #         ps.append({
        #             "name":p.name,
        #             "id":p.id,
        #             "compute_id":p.processor_operating['compute_node']['id']
        #         })
        #     processors = Cameras.objects(owner=user['email'])
        #     for p in processors:
        #         ps.append({
        #             "name":p.name,
        #             "id":str(p.id),
        #             "compute_id":p.compute_id,
        #             "group_name":p.group_name
        #         })
        #     c_node = []
        #     for c in nodes:
        #         c_node.append({
        #             "name": c.name,
        #             "id": c.id,
        #             "online":c.online,
        #             "memory":{
        #                 "used":c.memory.used,
        #                 "free":c.memory.free,
        #                 "total":c.memory.total
        #             },
        #             "disk":{
        #                 "used":c.disk.used,
        #                 "free":c.disk.free,
        #                 "total":c.disk.total
        #             },
        #             "cpu":{
        #                 "used_per_cpu":c.cpu.used_per_cpu,
        #                 "used":c.cpu.used
        #             }
        #         })
        #     nodes = ComputeNodes.objects(owner=user['email'])
        #     for c in nodes:
        #         c_node.append({
        #             "name": c.name,
        #             "id": str(c.id),
        #             "online":c.online,
        #             "memory":{
        #                 "used":c.memory.used,
        #                 "free":c.memory.free,
        #                 "total":c.memory.total
        #             },
        #             "disk":{
        #                 "used":c.disk.used,
        #                 "free":c.disk.free,
        #                 "total":c.disk.total
        #             },
        #             "cpu":{
        #                 "used_per_cpu":c.cpu.used_per_cpu,
        #                 "used":c.cpu.used
        #             }
        #         })    
        #     data = {
        #         "processors": ps,
        #         "compute_node": c_node
        #     }
        # else:
        try:
            processors = Cameras.objects(owner=user['email'])
            ps = []
            for p in processors:
                ps.append({
                    "name":p.name,
                    "id":str(p.id),
                    "compute_id":p.compute_id,
                    "group_name":p.group_name,
                })
            nodes = ComputeNodes.objects(owner=user['email'])
            c_node = []
            for c in nodes:
                c_node.append({
                    "name": c.name,
                    "id": str(c.id),
                    "online":c.online,
                    "key":c.key,
                    "memory":{
                        "used":c.memory.used,
                        "free":c.memory.free,
                        "total":c.memory.total
                    },
                    "disk":{
                        "used":c.disk.used,
                        "free":c.disk.free,
                        "total":c.disk.total
                    },
                    "cpu":{
                        "used_per_cpu":c.cpu.used_per_cpu,
                        "used":c.cpu.used
                    }
                })
            data = {
                "processors": ps,
                "compute_node": c_node
            }
        except:
            data = {
                "processors": " ",
                "compute_node": " "
            }
        encoded_jwt = jwt.encode( data,  salt, algorithm='HS256', headers={'message': 'OK'})
        return {"test": encoded_jwt.decode("utf-8")}
    def post(self):
        p = request.form['data']
        data = p.encode('utf8')
        data = jwt.decode(data, salt, algorithms=['HS256'])
        access_token = data['access_token'][0]
        user = check_token(access_token)
        lettersAndDigits = string.ascii_letters + string.digits
        key = ''.join(random.choice(lettersAndDigits) for i in range(10))
        compute = ComputeNodes(
            name = data['name'],
            owner = user['email'],
            key = key
        )
        compute.save()
        compute = ComputeNodes.objects(owner=user['email'], name=data['name']).first()
        com_id = str(compute.id)
        for c_id in data['cameras']:
            camera = Cameras.objects(id=c_id).first()
            camera.update(set__compute_id=com_id)
        encoded_jwt = jwt.encode( data,  salt, algorithm='HS256', headers={'message': 'OK'})
        return {"test": encoded_jwt.decode("utf-8")}
        
class PROCESSOR_RESOURCE(Resource):
    def put(self):
        p = request.form['data']
        data = p.encode('utf8')
        data = jwt.decode(data, salt, algorithms=['HS256'])
        name = data['name']
        owner = data['owner']
        key = data['key']
        compute = ComputeNodes.objects(name = name, owner= owner, key=key).first()
        compute.update(set__online=data['online'])
        compute.update(set__update_date=datetime.now())
        compute.update(set__memory__used=data['memory']['used'])
        compute.update(set__memory__free=data['memory']['free'])
        compute.update(set__memory__total=data['memory']['total'])
        compute.update(set__disk__used=data['disk']['used'])
        compute.update(set__disk__free=data['disk']['free'])
        compute.update(set__disk__total=data['disk']['total'])
        compute.update(set__cpu__used=data['cpu']['used'])
        compute.update(set__cpu__used_per_cpu=data['cpu']['used_per_cpu'])
        encoded_jwt = jwt.encode( data,  salt, algorithm='HS256', headers={'message': 'OK'})
        return {"test": encoded_jwt.decode("utf-8")}   


class VideoCamera(object):
    def __init__(self, uri):
        self.video = cv2.VideoCapture(uri)


    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()
        
def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

class TEST(Resource):
    def get(self):
        p = request.form['data']
        data = p.encode('utf8')
        data = jwt.decode(data, salt, algorithms=['HS256'])
        encoded_jwt = jwt.encode( data,  salt, algorithm='HS256', headers={'message': 'OK'})
        cameras = Cameras.objects(id =data['camera_id']).first()
        data = {
            'camera_uri':cameras.uri
        }
        encoded_jwt = jwt.encode( data,  salt, algorithm='HS256', headers={'message': 'OK'})
        return {"test": encoded_jwt.decode("utf-8")}

class SharedCamera(Resource):
    def get(self):
        p = request.form['data']
        data = p.encode('utf8')
        data = jwt.decode(data, salt, algorithms=['HS256'])
        encoded_jwt = jwt.encode( data,  salt, algorithm='HS256', headers={'message': 'OK'})
        access_token = data['access_token'][0]
        user = check_token(access_token)
        shared_list = SharedCameras.objects(shared=user['email'])
        data_email = []
        count = 0
        for i in shared_list:
            camera = Cameras.objects(id = i.camera_id)
            if camera:
                for c in camera:
                    data_email.append({
                        'camera_id':str(c.id),
                        'name':c.name,
                        'owner':c.owner
                    })
        user = MyUsers.objects(email = user['email']).first()
        shared_list = SharedCameras.objects(shared=user['permission'])
        data_permission = []
        for i in shared_list:
            camera = Cameras.objects(id = i.camera_id)
            if camera:
                for c in camera:
                    data_permission.append({
                        'camera_id':str(c.id),
                        'name':c.name,
                        'owner':c.owner
                    })
        data = {
            "email":data_email,
            "count_email":len(data_email),
            "permission":data_permission,
            "count_permission":len(data_permission)
        }
        print(data)
        encoded_jwt = jwt.encode( data,  salt, algorithm='HS256', headers={'message': 'OK'})
        return {"test": encoded_jwt.decode("utf-8")}

    def post(self):
        p = request.form['data']
        data = p.encode('utf8')
        data = jwt.decode(data, salt, algorithms=['HS256'])
        access_token = data['access_token'][0]
        user = check_token(access_token)
        if data['shared']:
            shared_camera = SharedCameras(
                camera_id = data['camera_id'],
                shared = data['shared']
            )
            shared_camera.save()
        print(data['shared_list'])
        if data['shared_list'] != []:
            for l in data['shared_list']:
                check_shared_camera = SharedCameras.objects(camera_id=data['camera_id'], shared=l).first()
                if check_shared_camera == None:
                    shared_camera = SharedCameras(
                        camera_id = data['camera_id'],
                        shared = l
                    )
                    shared_camera.save()
        encoded_jwt = jwt.encode( data,  salt, algorithm='HS256', headers={'message': 'OK'})
        return {"test": encoded_jwt.decode("utf-8")}
    def delete(self):
        p = request.form['data']
        data = p.encode('utf8')
        data = jwt.decode(data, salt, algorithms=['HS256'])
        access_token = data['access_token'][0]
        user = check_token(access_token)
        camera_id = data['camera_id']
        shared = data['shared']
        shared = SharedCameras.objects(camera_id=camera_id, shared=shared).first()
        shared.delete()
        encoded_jwt = jwt.encode( data,  salt, algorithm='HS256', headers={'message': 'OK'})
        return {"test": encoded_jwt.decode("utf-8")}

class PERMISSIONLIST(Resource):
    def get(self):
        p = request.form['data']
        data = p.encode('utf8')
        data = jwt.decode(data, salt, algorithms=['HS256'])
        encoded_jwt = jwt.encode( data,  salt, algorithm='HS256', headers={'message': 'OK'})
        access_token = data['access_token'][0]
        user = check_token(access_token)
        if user != None:
            permission = PermissionList.objects()
            permission_list = []
            for p in permission:
                permission_list.append(p.permission)
            data = {
                "permission_list": permission_list
            }
            print(data)
            encoded_jwt = jwt.encode( data,  salt, algorithm='HS256', headers={'message': 'OK'})
            return {"test": encoded_jwt.decode("utf-8")}

class ADMIN_USER(Resource):
    def get(self):
        p = request.form['data']
        data = p.encode('utf8')
        data = jwt.decode(data, salt, algorithms=['HS256'])
        access_token = data['access_token'][0]
        check = check_token(access_token)
        check_user = MyUsers.objects(email=check['email']).first()
        if check_user['permission'] == 'admin':
            users = MyUsers.objects()
            data = []
            for user in users:
                data.append(
                    {
                        'id': str(user.id),
                        'name' : user.name,
                        'email' : user.email,
                        'picture' : user.picture,
                        'permission' : user.permission,
                        'access_date' : str(user.access_date),
                        'last_access': str(user.last_access)
                    }
                )
            data = {
                "data":data
            }
            encoded_jwt = jwt.encode( data,  salt, algorithm='HS256', headers={'message': 'OK'})
            return {"test": encoded_jwt.decode("utf-8")}
        else:
            encoded_jwt = jwt.encode( data,  salt, algorithm='HS256', headers={'message': 'OK'})
            return {"test": encoded_jwt.decode("utf-8")}
    def post(self):
        p = request.form['data']
        data = p.encode('utf8')
        data = jwt.decode(data, salt, algorithms=['HS256'])
        access_token = data['access_token'][0]
        check = check_token(access_token)
        check_user = MyUsers.objects(email=check['email']).first()
        print(data['user_permission'])
        if check_user['permission'] == 'admin':
            users = MyUsers.objects(id=data['user_id']).first()
            users.update(set__permission=data['user_permission'])
        encoded_jwt = jwt.encode( data,  salt, algorithm='HS256', headers={'message': 'OK'})
        return {"test": encoded_jwt.decode("utf-8")}

class ADMIN_CAMERAS(Resource):
    def get(self):
        p = request.form['data']
        data = p.encode('utf8')
        data = jwt.decode(data, salt, algorithms=['HS256'])
        access_token = data['access_token'][0]
        check = check_token(access_token)
        check_user = MyUsers.objects(email=check['email']).first()
        if check_user['permission'] == 'admin':
            cameras = Cameras.objects()
            data = []
            for camera in cameras:
                data.append(
                    {
                        'id': str(camera.id),
                        'uri' : camera.uri,
                        'owner' : camera.owner,
                        'create_date' : str(camera.create_date),
                        'name' : camera.name,
                        'update_date' : str(camera.update_date),
                    }
                )
            data = {
                "data":data
            }
            encoded_jwt = jwt.encode( data,  salt, algorithm='HS256', headers={'message': 'OK'})
            return {"test": encoded_jwt.decode("utf-8")}
        else:
            encoded_jwt = jwt.encode( data,  salt, algorithm='HS256', headers={'message': 'OK'})
            return {"test": encoded_jwt.decode("utf-8")}

class ADMIN_PROCESSORS(Resource):
    def get(self):
        p = request.form['data']
        data = p.encode('utf8')
        data = jwt.decode(data, salt, algorithms=['HS256'])
        access_token = data['access_token'][0]
        check = check_token(access_token)
        check_user = MyUsers.objects(email=check['email']).first()
        if check_user['permission'] == 'admin':
            nodes = ComputeNodes.objects()
            c_node = []
            for c in nodes:
                c_node.append({
                    "name": c.name,
                    "id": str(c.id),
                    "online":c.online,
                    "memory":{
                        "used":c.memory.used,
                        "free":c.memory.free,
                        "total":c.memory.total
                    },
                    "disk":{
                        "used":c.disk.used,
                        "free":c.disk.free,
                        "total":c.disk.total
                    },
                    "cpu":{
                        "used_per_cpu":c.cpu.used_per_cpu,
                        "used":c.cpu.used
                    },
                    "owner":c.owner,
                    "create_date":str(c.create_date),
                    "update_date":str(c.update_date),
                    "memory_used_percent": int(c.memory.used/c.memory.total*100),
                    "disk_used_percent": int(c.disk.used/c.disk.total*100),
                })
            data = {
                "data":c_node
            }
            encoded_jwt = jwt.encode( data,  salt, algorithm='HS256', headers={'message': 'OK'})
            return {"test": encoded_jwt.decode("utf-8")}
        else:
            encoded_jwt = jwt.encode( data,  salt, algorithm='HS256', headers={'message': 'OK'})
            return {"test": encoded_jwt.decode("utf-8")}

class ADMIN_GET_PROCESSORS(Resource):
    def get(self):
        p = request.form['data']
        data = p.encode('utf8')
        data = jwt.decode(data, salt, algorithms=['HS256'])
        encoded_jwt = jwt.encode( data,  salt, algorithm='HS256', headers={'message': 'OK'})
        access_token = data['access_token'][0]
        if len(access_token) < 5:
            access_token = data['access_token']
        user = check_token(access_token)
        user = MyUsers.objects(email=user['email']).first()
        try:
            nodes = ComputeNodes.objects(owner=user['email'])
            c_node = []
            for c in nodes:
                c_node.append({
                    "name": c.name,
                    "id": str(c.id),
                    "online":c.online,
                    "memory":{
                        "used":c.memory.used,
                        "free":c.memory.free,
                        "total":c.memory.total
                    },
                    "disk":{
                        "used":c.disk.used,
                        "free":c.disk.free,
                        "total":c.disk.total
                    },
                    "cpu":{
                        "used_per_cpu":c.cpu.used_per_cpu,
                        "used":c.cpu.used
                    },
                    "update_date":str(c.update_date),
                    
                })
            data = {
                "compute_node": c_node
            }
        except:
            data = {
                "processors": " ",
                "compute_node": " "
            }
        encoded_jwt = jwt.encode( data,  salt, algorithm='HS256', headers={'message': 'OK'})
        return {"test": encoded_jwt.decode("utf-8")}


api.add_resource(MY_NAME, '/name')
api.add_resource(USER, '/user')
api.add_resource(CAMERA, '/camera')
api.add_resource(CAMERAS, '/cameras')
api.add_resource(CAMERAS_IN_GROUP, '/cameras_in_group')
api.add_resource(GROUP, '/group')
api.add_resource(GROUPS, '/groups')
api.add_resource(PROCESSOR, '/processor')
api.add_resource(PROCESSORS, '/processors')
api.add_resource(PROCESSOR_RESOURCE, '/processors_resource')
api.add_resource(SharedCamera, '/shared_camera')
api.add_resource(PERMISSIONLIST, '/permission_list')
api.add_resource(TEST, '/test')

api.add_resource(ADMIN_USER, '/admin_users')
api.add_resource(ADMIN_CAMERAS, '/admin_cameras')
api.add_resource(ADMIN_PROCESSORS, '/admin_processors')
api.add_resource(ADMIN_GET_PROCESSORS, '/admin_get_processors')