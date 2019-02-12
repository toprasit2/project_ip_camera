import os
# import secrets
from flask import  render_template, url_for, flash, redirect, request, abort, session, jsonify, Markup, Response
import cv2
from camera import app, bcrypt, google
from camera.forms import RegistrationForm, LoginForm, GroupOfCamerasForm, CamerasForm, ComputeForm, SharewithUserForm, UserPermissionForm
# from camera.models import Users, Cameras, GroupOfCameras
# from flask_login import login_user, current_user, logout_user, login_required
import requests
import json
import jwt
from nokkhumclient import client


salt = 'อิอิอุอิ'


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

def get_user():
    if 'google_token' in session:
        me = google.get('userinfo')
        if 'error' in me.data:
            return 'error'
        else:
            if 'name' in me.data:
                name = me.data['name']
            else:
                name = me.data['email']
            data = {
                'name': name,
                'email': me.data['email'],
                'picture': me.data['picture']
            }
        user =jwt.encode( data,  salt, algorithm='HS256', headers={'message': 'OK'})
        r = requests.get("http://127.0.0.1:7000/api/user", data={'data':user.decode('utf8')})
        r_data = json.loads(r.text)['test'].encode('utf8')
        user = jwt.decode(r_data, salt, algorithms=['HS256'])
        return user
    return redirect(url_for('login'))

def get_groups():
    if 'google_token' in session:
        me = google.get('userinfo')
        if 'error' in me.data:
            return 'error'
        else:
            if 'name' in me.data:
                name = me.data['name']
            else:
                name =  me.data['email']
            data = {
                'name': name,
                'email': me.data['email'],
                'picture': me.data['picture'],
                'access_token': session['google_token'],
            }
        groups =jwt.encode( data,  salt, algorithm='HS256', headers={'message': 'OK'})
        r = requests.get("http://127.0.0.1:7000/api/groups", data={'data':groups.decode('utf8')})
        r_data = json.loads(r.text)['test'].encode('utf8')
        groups = jwt.decode(r_data, salt, algorithms=['HS256'])
        if 'error' in groups:
            groups = []
        else:
            groups = groups['data']
        cameras = get_cameras()
        for g in groups:
            g['count'] = 0
            g['cameras'] = []
            for c in cameras:
                if g['group_name'] == c['group_name']:
                    g['count']+=1
                    g['cameras'].append(c)

            count = int(g['count']/1)
            check = g['count']/1
            if count - check != 0:
                g['display_1x1'] = int(g['count']/1)+1
            else:
                g['display_1x1'] = int(g['count']/1)
            cameras_1x1 = [g['cameras'][x:x+1] for x in range(0, len(g['cameras']),1)]
            g['cameras_1x1'] = cameras_1x1

            count = int(g['count']/4)
            check = g['count']/4
            if count - check != 0:
                g['display_2x2'] = int(g['count']/4)+1
            else:
                g['display_2x2'] = int(g['count']/4)
            cameras_2x2 = [g['cameras'][x:x+4] for x in range(0, len(g['cameras']),4)]
            g['cameras_2x2'] = cameras_2x2

            count = int(g['count']/9)
            check = g['count']/9
            if count - check != 0:
                g['display_3x3'] = int(g['count']/9)+1
            else:
                g['display_3x3'] = int(g['count']/9)
            cameras_3x3 = [g['cameras'][x:x+9] for x in range(0, len(g['cameras']),9)]
            g['cameras_3x3'] = cameras_3x3

            count = int(g['count']/16)
            check = g['count']/16
            if count - check != 0:
                g['display_4x4'] = int(g['count']/16)+1
            else:
                g['display_4x4'] = int(g['count']/16)
            cameras_4x4 = [g['cameras'][x:x+16] for x in range(0, len(g['cameras']),16)]
            g['cameras_4x4'] = cameras_4x4
        return groups
    return redirect(url_for('login'))

def get_cameras():
    if 'google_token' in session:
        me = google.get('userinfo')
        if 'error' in me.data:
            return 'error'
        else:
            if 'name' in me.data:
                name = me.data['name']
            else:
                name =  me.data['email']
            data = {
                'name': name,
                'email': me.data['email'],
                'picture': me.data['picture'],
                'access_token': session['google_token'],
            }
        cameras =jwt.encode( data,  salt, algorithm='HS256', headers={'message': 'OK'})
        r = requests.get("http://127.0.0.1:7000/api/cameras", data={'data':cameras.decode('utf8')})
        r_data = json.loads(r.text)['test'].encode('utf8')
        cameras = jwt.decode(r_data, salt, algorithms=['HS256'])
        if 'error' in cameras:
            cameras = []
        else:
            cameras = cameras['data']
        return cameras
    return redirect(url_for('login'))

def get_cameras_in_group(group):
    if 'google_token' in session:
        me = google.get('userinfo')
        if 'error' in me.data:
            return 'error'
        else:
            if 'name' in me.data:
                name = me.data['name']
            else:
                name =  me.data['email']
            data = {
                'name': name,
                'email': me.data['email'],
                'picture': me.data['picture'],
                'group_id': group,
                'access_token': session['google_token'],
            }
        cameras =jwt.encode( data,  salt, algorithm='HS256', headers={'message': 'OK'})
        r = requests.get("http://127.0.0.1:7000/api/cameras_in_group", data={'data':cameras.decode('utf8')})
        r_data = json.loads(r.text)['test'].encode('utf8')
        cameras = jwt.decode(r_data, salt, algorithms=['HS256'])
        if 'error' in cameras:
            cameras = []
        else:
            cameras = cameras['data']
        return cameras
    return redirect(url_for('login'))

def get_group(group):
    if 'google_token' in session:
        me = google.get('userinfo')
        if 'error' in me.data:
            return 'error'
        else:
            if 'name' in me.data:
                name = me.data['name']
            else:
                name =  me.data['email']
            data = {
                'name': name,
                'email': me.data['email'],
                'picture': me.data['picture'],
                'group_id': group,
                'access_token': session['google_token'],                
            }
        groups =jwt.encode( data,  salt, algorithm='HS256', headers={'message': 'OK'})
        r = requests.get("http://127.0.0.1:7000/api/group", data={'data':groups.decode('utf8')})
        r_data = json.loads(r.text)['test'].encode('utf8')
        groups = jwt.decode(r_data, salt, algorithms=['HS256'])
        if 'error' in groups:
            groups = []
        else:
            groups = groups
        return groups
    return redirect(url_for('login'))

def get_processors():
    if 'google_token' in session:
        me = google.get('userinfo')
        if 'error' in me.data:
            return redirect(url_for('logout'))
        nk = nokkhum_client()
        processors = nk.admin.processors.list()
    return processors

def get_compute_nodes():
    if 'google_token' in session:
        me = google.get('userinfo')
        if 'error' in me.data:
            return redirect(url_for('logout'))
        nk = nokkhum_client()
        compute_node = nk.admin.compute_nodes.list()
    return compute_node

def get_nodes(id):
    if 'google_token' in session:
        me = google.get('userinfo')
        if 'error' in me.data:
            return redirect(url_for('logout'))
        nk = nokkhum_client()
        compute_node = nk.admin.compute_nodes.get(id)
    return compute_node

def get_shared_cameras():
    data = {
        'access_token': session['google_token'],
    }
    permission =jwt.encode( data,  salt, algorithm='HS256', headers={'message': 'OK'})
    r = requests.get("http://127.0.0.1:7000/api/permission_list", data={'data':permission.decode('utf8')})
    r_data = json.loads(r.text)['test'].encode('utf8')
    permission_list = jwt.decode(r_data, salt, algorithms=['HS256'])
    shared_camera =jwt.encode( data,  salt, algorithm='HS256', headers={'message': 'OK'})
    r = requests.get("http://127.0.0.1:7000/api/shared_camera", data={'data':shared_camera.decode('utf8')})
    r_data = json.loads(r.text)['test'].encode('utf8')
    shared_camera = jwt.decode(r_data, salt, algorithms=['HS256'])
    s = {}

    count = int(shared_camera['count_email']/1)
    check = shared_camera['count_email']/1
    if count - check != 0:
        s['email_display_1x1'] = int(shared_camera['count_email']/1)+1
    else:
        s['email_display_1x1'] = int(shared_camera['count_email']/1)
    cameras_1x1 = [shared_camera['email'][x:x+1] for x in range(0, len(shared_camera['email']),1)]
    s['email_cameras_1x1'] = cameras_1x1

    count = int(shared_camera['count_email']/4)
    check = shared_camera['count_email']/4
    if count - check != 0:
        s['email_display_2x2'] = int(shared_camera['count_email']/4)+1
    else:
        s['email_display_2x2'] = int(shared_camera['count_email']/4)
    cameras_2x2 = [shared_camera['email'][x:x+4] for x in range(0, len(shared_camera['email']),4)]
    s['email_cameras_2x2'] = cameras_2x2

    count = int(shared_camera['count_email']/9)
    check = shared_camera['count_email']/9
    if count - check != 0:
        s['email_display_3x3'] = int(shared_camera['count_email']/9)+1
    else:
        s['email_display_3x3'] = int(shared_camera['count_email']/9)
    cameras_3x3 = [shared_camera['email'][x:x+9] for x in range(0, len(shared_camera['email']),9)]
    s['email_cameras_3x3'] = cameras_3x3

    count = int(shared_camera['count_email']/16)
    check = shared_camera['count_email']/16
    if count - check != 0:
        s['email_display_4x4'] = int(shared_camera['count_email']/16)+1
    else:
        s['email_display_4x4'] = int(shared_camera['count_email']/16)
    cameras_4x4 = [shared_camera['email'][x:x+16] for x in range(0, len(shared_camera['email']),16)]
    s['email_cameras_4x4'] = cameras_4x4
    
    count = int(shared_camera['count_permission']/1)
    check = shared_camera['count_permission']/1
    if count - check != 0:
        s['permission_display_1x1'] = int(shared_camera['count_permission']/1)+1
    else:
        s['permission_display_1x1'] = int(shared_camera['count_permission']/1)
    cameras_1x1 = [shared_camera['email'][x:x+1] for x in range(0, len(shared_camera['email']),1)]
    s['permission_cameras_1x1'] = cameras_1x1
    
    count = int(shared_camera['count_permission']/4)
    check = shared_camera['count_permission']/4
    if count - check != 0:
        s['permission_display_2x2'] = int(shared_camera['count_permission']/4)+1
    else:
        s['permission_display_2x2'] = int(shared_camera['count_permission']/4)
    cameras_2x2 = [shared_camera['permission'][x:x+4] for x in range(0, shared_camera['count_permission'],4)]
    s['permission_cameras_2x2'] = cameras_2x2

    count = int(shared_camera['count_permission']/9)
    check = shared_camera['count_permission']/9
    if count - check != 0:
        s['permission_display_3x3'] = int(shared_camera['count_permission']/9)+1
    else:
        s['permission_display_3x3'] = int(shared_camera['count_permission']/9)
    cameras_3x3 = [shared_camera['permission'][x:x+9] for x in range(0, shared_camera['count_permission'],9)]
    s['permission_cameras_3x3'] = cameras_3x3

    count = int(shared_camera['count_permission']/16)
    check = shared_camera['count_permission']/16
    if count - check != 0:
        s['permission_display_4x4'] = int(shared_camera['count_permission']/16)+1
    else:
        s['permission_display_4x4'] = int(shared_camera['count_permission']/16)
    cameras_4x4 = [shared_camera['permission'][x:x+16] for x in range(0, shared_camera['count_permission'],16)]
    s['permission_cameras_4x4'] = cameras_4x4

    s['email'] = shared_camera['email']
    s['count_email'] = shared_camera['count_email']
    s['permission'] = shared_camera['permission']
    s['count_permission'] = shared_camera['count_permission']
    return s

@app.route('/')
def index():
    if 'google_token' in session:
        me = google.get('userinfo')
        if 'error' in me.data:
            return redirect(url_for('logout'))
        return redirect(url_for('cameras'))
    return redirect(url_for('login'))

@app.route('/home')
def home():
    if 'google_token' in session:
        user = get_user()
        if user == 'error':
            return redirect(url_for('logout'))
        groups = get_groups()
        cameras = get_cameras()
        labels = ["January","February","March","April","May","June","July","August"]
        values = [10,9,8,7,6,4,7,8]
        home = {
            'active':"active"
        }
        return render_template('home.html', user=user, set=zip(values, labels), home=home, groups=groups, cameras=cameras)
    return "NO"

@app.route('/login')
def login():
    return google.authorize(callback=url_for('authorized', _external=True))

@app.route('/logout')
def logout():
    session.pop('google_token', None)
    return redirect(url_for('index'))

@app.route('/login/authorized')
def authorized():
    resp = google.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    # print(resp)
    session['google_token'] = (resp['access_token'], ' ')
    return redirect(url_for('add_user'))

@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')

@app.route('/add_user')
def add_user():
    if 'google_token' in session:
        me = google.get('userinfo')
        if 'error' in me.data:
            return 'error'
        if 'name' in me.data:
            name = me.data['name']
            if name == '':
                name = me.data['email']
        else:
            name = me.data['email']
        data = {
            'name': name,
            'email': me.data['email'],
            'picture': me.data['picture']
        }
        user =jwt.encode( data,  salt, algorithm='HS256', headers={'message': 'OK'})
        r = requests.post("http://127.0.0.1:7000/api/user", data={'data':user.decode('utf8')})
        r_status = json.loads(r.text)['status']
        if r_status == "200":
            flash('welcome '+name, 'green lighten-2')
        return redirect(url_for('cameras'))

@app.route('/cameras')
def cameras():
    if 'google_token' in session:
        user = get_user()
        if user == 'error':
            return redirect(url_for('logout'))
        groups = get_groups()
        data = {
            'access_token': session['google_token'],
        }
        permission =jwt.encode( data,  salt, algorithm='HS256', headers={'message': 'OK'})
        r = requests.get("http://127.0.0.1:7000/api/permission_list", data={'data':permission.decode('utf8')})
        r_data = json.loads(r.text)['test'].encode('utf8')
        permission_list = jwt.decode(r_data, salt, algorithms=['HS256'])
        shared_camera = get_shared_cameras()
        permission_list = permission_list['permission_list']
        # composite_list = [cameras[x:x+2] for x in range(0, len(cameras),2)]
        # for i in composite_list:
        #     print(i)
        return render_template('cameras_all.html', title="Camearas", groups=groups, user=user, permission_list=permission_list, shared_camera=shared_camera)
    return render_template('cameras_all.html', title="Camearas")

@app.route('/cameras/<group_id>/<display>', methods=['GET', 'POST'])
def camera(group_id, display):
    back = request.args.get('next')
    if 'google_token' in session:
        user = get_user()
        if user == 'error':
            return redirect(url_for('logout'))
        groups = get_groups()
        group = get_group(group_id)
        camera_status = {
            'active': 'active'
        }
        share_form = SharewithUserForm()
        if request.method == 'POST':
            camera_id = request.args.get('camera_id')
            data = { 
                'access_token': session['google_token'],
                'camera_id': camera_id,
                'shared': share_form.email.data,
                'shared_list': share_form.permission_list.data
            }
            # print(data)
            cameras =jwt.encode( data,  salt, algorithm='HS256', headers={'message': 'OK'})
            r = requests.post("http://127.0.0.1:7000/api/shared_camera", data={'data':cameras.decode('utf8')})
            # print(camera_id, share_form.email.data, share_form.permission_list.data)
            return redirect(back)

        data = {
            'access_token': session['google_token'],
        }
        permission =jwt.encode( data,  salt, algorithm='HS256', headers={'message': 'OK'})
        r = requests.get("http://127.0.0.1:7000/api/permission_list", data={'data':permission.decode('utf8')})
        r_data = json.loads(r.text)['test'].encode('utf8')
        permission_list = jwt.decode(r_data, salt, algorithms=['HS256'])
        permission_list = permission_list['permission_list']
        choice = []
        for c in permission_list:
            choice.append((c,c))
        share_form.permission_list.choices = choice
        shared_camera = get_shared_cameras()
        return render_template('cameras_in_group.html', title="Camera", user=user, group_id=group_id, camera_status=camera_status, groups=groups, group=group, display=display, share_form=share_form, shared_camera=shared_camera, permission_list=permission_list)
    return redirect(url_for('index'))

@app.route('/add_camera/<group_name>', methods=['GET', 'POST'])
def add_camera(group_name):
    back = request.args.get('next')
    if 'google_token' in session:
        user = get_user()
        if user == 'error':
            return redirect(url_for('logout'))
        form = CamerasForm()
        form.owner.data = user['email']
        form.group_name.data = group_name
        if form.validate_on_submit():
            data = { 
                "group_name":form.group_name.data,
                "owner":form.owner.data,
                "name":form.name.data,
                "description":form.description.data,
                "uri":form.uri.data,
                "refresh":form.refresh.data
                # "port":form.port.data, 
                # "password":form.password.data, 
                # "username":form.username.data
            }
            # print(data)
            cameras =jwt.encode( data,  salt, algorithm='HS256', headers={'message': 'OK'})
            r = requests.post("http://127.0.0.1:7000/api/camera", data={'data':cameras.decode('utf8')})
            r_data = json.loads(r.text)['test'].encode('utf8')
            cameras = jwt.decode(r_data, salt, algorithms=['HS256'])
            flash(cameras["name"] + ' added', 'green lighten-2')
            return redirect(back)
        return render_template("add_camera.html", title="Add Camera", form=form, user=user,back=back,group_name=group_name)


@app.route('/add_group', methods=['GET', 'POST'])
def add_group():
    back = request.args.get('next')
    user = get_user()
    if user == 'error':
        return redirect(url_for('logout'))
    form = GroupOfCamerasForm()
    form.owner.data = user['email']
    if form.validate_on_submit():
        data = {
            "owner":form.owner.data, 
            "group_name":form.group_name.data,
            'access_token': session['google_token'],    
            # "c_lat":form.c_lat.data,
            # "c_long":form.c_long.data,
        }
        groups =jwt.encode( data,  salt, algorithm='HS256', headers={'message': 'OK'})
        r = requests.post("http://127.0.0.1:7000/api/group", data={'data':groups.decode('utf8')})
        r_data = json.loads(r.text)['test'].encode('utf8')
        groups = jwt.decode(r_data, salt, algorithms=['HS256'])
        flash('Group '+ groups["group_name"] +' added', 'green lighten-2')
        return redirect(back)
    return render_template('add_group.html', title="Cameras", form=form, user=user, back=back)


@app.route('/edit_group/<group_id>/<group_name>', methods=['GET', 'POST'])
def edit_group(group_id, group_name):
    back = request.args.get('next')
    if 'google_token' in session:
        user = get_user()
        if user == 'error':
            return redirect(url_for('logout'))
        form = GroupOfCamerasForm()
        form.owner.data = user['email']
        if form.validate_on_submit():
            data = { 
                "group_id":group_id,
                "group_name":form.group_name.data,
                "access_token":session['google_token'],
                # "port":form.port.data, 
                # "password":form.password.data, 
                # "username":form.username.data
            }
            # print(data)
            group =jwt.encode( data,  salt, algorithm='HS256', headers={'message': 'OK'})
            r = requests.put("http://127.0.0.1:7000/api/group", data={'data':group.decode('utf8')})
            return redirect(back)
        group = get_group(group_id)
        form.group_name.data = group_name   
    return render_template('edit_group.html', title="Edit", form=form, user=user,back=back,group_name=group_name)

@app.route('/delete_group/<group_id>/<group_name>', methods=['GET', 'POST'])
def delete_group(group_id, group_name):
    back = request.args.get('next')
    data = {
            "group_id":group_id,
    }
    groups =jwt.encode( data,  salt, algorithm='HS256', headers={'message': 'OK'})
    r = requests.delete("http://127.0.0.1:7000/api/group", data={'data':groups.decode('utf8')})
    r_data = json.loads(r.text)['test'].encode('utf8')
    flash(group_name + ' has deleted', 'green lighten-2')
    return  redirect(url_for('cameras'))

@app.route('/edit_camera/<camera_id>/<group_name>', methods=['GET', 'POST'])
def edit_camera(camera_id, group_name):
    back = request.args.get('next')
    if 'google_token' in session:
        user = get_user()
        if user == 'error':
            return redirect(url_for('logout'))
        form = CamerasForm()
        form.owner.data = user['email']
        form.group_name.data = group_name
        if form.validate_on_submit():
            data = { 
                "camera_id":camera_id,
                "group_name":form.group_name.data,
                "name":form.name.data,
                "description":form.description.data,
                "uri":form.uri.data,
                "refresh":form.refresh.data,
                "access_token":session['google_token'],
            }
            #print(data)
            cameras =jwt.encode( data,  salt, algorithm='HS256', headers={'message': 'OK'})
            # print(cameras)
            r = requests.put("http://127.0.0.1:7000/api/camera", data={'data':cameras.decode('utf8')})
            return redirect(back)
        data = {
            "camera_id":camera_id,
        }
        groups =jwt.encode( data,  salt, algorithm='HS256', headers={'message': 'OK'})
        r = requests.get("http://127.0.0.1:7000/api/camera", data={'data':groups.decode('utf8')})
        r_data = json.loads(r.text)['test'].encode('utf8')
        cameras = jwt.decode(r_data, salt, algorithms=['HS256'])
        cameras = cameras['data']
        for camera in cameras:
            form.group_name.data = camera['group_name']
            form.owner.data = camera['owner']
            form.name.data = camera['name']
            form.description.data = camera['description']
            form.uri.data = camera['uri']
            form.refresh.data = camera['refresh']
            camera_name = camera['name']
        
    return render_template('add_camera.html', title="Edit", form=form, user=user,back=back,camera_name=camera_name)

@app.route('/delete_camera/<camera_id>/<camera_name>', methods=['GET', 'POST'])
def delete_camera(camera_id, camera_name):
    back = request.args.get('next')
    data = {
            "camera_id":camera_id,
        }
    groups =jwt.encode( data,  salt, algorithm='HS256', headers={'message': 'OK'})
    r = requests.delete("http://127.0.0.1:7000/api/camera", data={'data':groups.decode('utf8')})
    r_data = json.loads(r.text)['test'].encode('utf8')
    flash(camera_name + ' has deleted', 'green lighten-2')
    return redirect(back)

@app.route('/processors', methods=['GET', 'POST'])
def processors():
    if 'google_token' in session:
        user = get_user()
        if user == 'error':
            return redirect(url_for('logout'))
        data = {
            'access_token': session['google_token'],
        }
        groups =jwt.encode( data,  salt, algorithm='HS256', headers={'message': 'OK'})
        r = requests.get("http://127.0.0.1:7000/api/processors", data={'data':groups.decode('utf8')})
        r_data = json.loads(r.text)['test'].encode('utf8')
        data = jwt.decode(r_data, salt, algorithms=['HS256'])
        # print(data)
        processors = data['processors']
        compute_nodes = data['compute_node']
        my_token = session['google_token'][0]
        return render_template('processors.html', title="Processors",user=user, processors=processors, compute_nodes=compute_nodes, my_token=my_token)
    return redirect(url_for('login'))

@app.route('/add_compute', methods=['GET', 'POST'])
def add_compute():
    back = request.args.get('next')
    user = get_user()
    if user == 'error':
        return redirect(url_for('logout'))
    cameras = get_cameras()
    form = ComputeForm()
    choice = []
    for c in cameras:
        choice.append((c['id'],c['group_name']+' '+c['name']))
    form.cameras.choices = choice
    if form.validate_on_submit():
        data = {
            "name":form.name.data,
            'access_token': session['google_token'],
            "cameras":form.cameras.data
        }
        processors =jwt.encode( data,  salt, algorithm='HS256', headers={'message': 'OK'})
        r = requests.post("http://127.0.0.1:7000/api/processors", data={'data':processors.decode('utf8')})
        r_data = json.loads(r.text)['test'].encode('utf8')
        processors = jwt.decode(r_data, salt, algorithms=['HS256'])
        flash('Group '+ form.name.data + ' added', 'green lighten-2')
        return redirect(back)
    return render_template('add_compute.html', title="Cameras", form=form, user=user, back=back)

@app.route('/get_processors', methods=['GET', 'POST'])
def get_processors():
    data = {
        'access_token': session['google_token'],
    }
    # print(session['google_token'])
    groups =jwt.encode( data,  salt, algorithm='HS256', headers={'message': 'OK'})
    r = requests.get("http://127.0.0.1:7000/api/processors", data={'data':groups.decode('utf8')})
    r_data = json.loads(r.text)['test'].encode('utf8')
    data = jwt.decode(r_data, salt, algorithms=['HS256'])
    return json.dumps(data)

@app.route('/edit_processor/<processor_id>', methods=['GET', 'POST'])
def edit_processor(processor_id):
    back = request.args.get('next')
    user = get_user()
    if user == 'error':
        return redirect(url_for('logout'))
    data = {
        "processor_id":processor_id,
        'access_token': session['google_token'],
    }
    processor =jwt.encode( data,  salt, algorithm='HS256', headers={'message': 'OK'})
    r = requests.get("http://127.0.0.1:7000/api/processor", data={'data':processor.decode('utf8')})
    r_data = json.loads(r.text)['test'].encode('utf8')
    processor = jwt.decode(r_data, salt, algorithms=['HS256'])
    form = ComputeForm()
    if form.name.data == None:
        form.name.data = processor['name']
    cameras = get_cameras()
    choice = []
    for c in cameras:
        choice.append((c['id'],c['group_name']+' '+c['name']))
    form.cameras.choices = choice
    default_choice = []
    for c in cameras:
        if c['compute_id'] == processor_id:
            default_choice.append(c['id'])
    if form.validate_on_submit():
        data = {
            "name":form.name.data,
            'access_token': session['google_token'],
            "cameras":form.cameras.data,
            "id":processor_id
        }
        processor = jwt.encode( data,  salt, algorithm='HS256', headers={'message': 'OK'})
        r = requests.put("http://127.0.0.1:7000/api/processor", data={'data':processor.decode('utf8')})
        return redirect(back)
    form.cameras.data = default_choice
    return render_template('add_compute.html', title="Cameras", form=form, user=user, back=back)

@app.route('/delete_processor/<processor_id>/<processor_name>', methods=['GET', 'POST'])
def delete_processor(processor_id, processor_name):
    back = request.args.get('next')
    data = {
        "processor_id":processor_id,
        'access_token': session['google_token'],
    }
    groups =jwt.encode( data,  salt, algorithm='HS256', headers={'message': 'OK'})
    r = requests.delete("http://127.0.0.1:7000/api/processor", data={'data':groups.decode('utf8')})
    flash(processor_name + ' has deleted', 'green lighten-2')
    return redirect(back)

@app.route('/shared_camera/<camera_id>/<time>', methods=['GET'])
def shared_camera(camera_id,time):
    if 'google_token' in session:
        user = get_user()
        if user == 'error':
            return redirect(url_for('logout'))
        data = {
            'camera_id': camera_id,
            'access_token': session['google_token'],
        }
        shared_camera_id =jwt.encode( data,  salt, algorithm='HS256', headers={'message': 'OK'})
        r =  requests.get("http://127.0.0.1:7000/api/test", data={'data':shared_camera_id.decode('utf8')})
        r_data = json.loads(r.text)['test'].encode('utf8')
        shared_camera = jwt.decode(r_data, salt, algorithms=['HS256'])
        return Response(gen(VideoCamera(uri=shared_camera['camera_uri'])),
                mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/shared_cameras/<select>/<display>', methods=['GET', 'POST'])
def shared_cameras(select, display):
    back = request.args.get('next')
    if 'google_token' in session:
        user = get_user()
        if user == 'error':
            return redirect(url_for('logout'))
        data = {
            'access_token': session['google_token'],
        }
        groups = get_groups()
        permission =jwt.encode( data,  salt, algorithm='HS256', headers={'message': 'OK'})
        r = requests.get("http://127.0.0.1:7000/api/permission_list", data={'data':permission.decode('utf8')})
        r_data = json.loads(r.text)['test'].encode('utf8')
        permission_list = jwt.decode(r_data, salt, algorithms=['HS256'])
        permission_list = permission_list['permission_list']
        shared_camera = get_shared_cameras()
        print(shared_camera)
        return render_template('shared_in_group.html', title="Camera", user=user, groups=groups, select=select, display=display, shared_camera=shared_camera,permission_list=permission_list)
    return redirect(url_for('index'))

@app.route('/delete_shared/<camera_id>/<shared>', methods=['GET', 'POST'])
def delete_shared(camera_id, shared):
    back = request.args.get('next')
    data = { 
        'access_token': session['google_token'],
        'camera_id': camera_id,
        'shared': shared
    }
    # print(data)
    cameras =jwt.encode( data,  salt, algorithm='HS256', headers={'message': 'OK'})
    r = requests.delete("http://127.0.0.1:7000/api/shared_camera", data={'data':cameras.decode('utf8')})
    return  redirect(back)

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

@app.route('/admin', methods=['GET'])
def admin():
    user = get_user()
    if 'google_token' in session and user['permission'] == 'admin':
        return render_template('admin_home.html', title="Admin Home", user=user)
    return redirect(url_for('index'))
    

@app.route('/admin/cameras_detail', methods=['GET'])
def admin_cameras_detail():
    back = request.args.get('next')
    user = get_user()
    if 'google_token' in session and user['permission'] == 'admin':
        
        data = {
            'access_token': session['google_token'],
        }
        cameras_all =jwt.encode( data,  salt, algorithm='HS256', headers={'message': 'OK'})
        r =  requests.get("http://127.0.0.1:7000/api/admin_cameras", data={'data':cameras_all.decode('utf8')})
        r_data = json.loads(r.text)['test'].encode('utf8')
        cameras_all = jwt.decode(r_data, salt, algorithms=['HS256'])
        cameras_all=cameras_all['data']
        count_cameras_all = len(cameras_all)
        return render_template('admin_cameras.html', title="Admin Home", user=user, back=back, cameras_all=cameras_all, count_cameras_all=count_cameras_all)
    return redirect(url_for('index'))

@app.route('/admin/users_detail', methods=['GET', 'POST'])
def admin_users_detail():
    back = request.args.get('next')
    user = get_user()
    if 'google_token' in session and user['permission'] == 'admin':
        
        data = {
            'access_token': session['google_token'],
        }
        users_all =jwt.encode( data,  salt, algorithm='HS256', headers={'message': 'OK'})
        r =  requests.get("http://127.0.0.1:7000/api/admin_users", data={'data':users_all.decode('utf8')})
        r_data = json.loads(r.text)['test'].encode('utf8')
        users_all = jwt.decode(r_data, salt, algorithms=['HS256'])
        users_all=users_all['data']
        user_form = UserPermissionForm()
        if request.method == 'POST':
            user_id = request.args.get('user_id')
            data = { 
                'access_token': session['google_token'],
                'user_id': user_id,
                'user_permission': user_form.permission_list.data
            }
            print(user_id, user_form.permission_list.data)
            user =jwt.encode( data,  salt, algorithm='HS256', headers={'message': 'OK'})
            r = requests.post("http://127.0.0.1:7000/api/admin_users", data={'data':user.decode('utf8')})
            return redirect(back)

        permission =jwt.encode( data,  salt, algorithm='HS256', headers={'message': 'OK'})
        r = requests.get("http://127.0.0.1:7000/api/permission_list", data={'data':permission.decode('utf8')})
        r_data = json.loads(r.text)['test'].encode('utf8')
        permission_list = jwt.decode(r_data, salt, algorithms=['HS256'])
        permission_list = permission_list['permission_list']
        choice = []
        for c in permission_list:
            choice.append((c,c))
        user_form.permission_list.choices = choice

        return render_template('admin_users.html', title="Admin Home", user=user, back=back, users_all=users_all, user_form=user_form)
    return redirect(url_for('index'))

@app.route('/admin/processors_detail', methods=['GET'])
def admin_processors_detail():
    back = request.args.get('next')
    user = get_user()
    if 'google_token' in session and user['permission'] == 'admin':
        
        data = {
            'access_token': session['google_token'],
        }
        processors_all =jwt.encode( data,  salt, algorithm='HS256', headers={'message': 'OK'})
        r =  requests.get("http://127.0.0.1:7000/api/admin_processors", data={'data':processors_all.decode('utf8')})
        r_data = json.loads(r.text)['test'].encode('utf8')
        processors_all = jwt.decode(r_data, salt, algorithms=['HS256'])
        processors_all=processors_all['data']
        return render_template('admin_processors.html', title="Admin Home", user=user, back=back, processors_all=processors_all)
    return redirect(url_for('index'))

@app.route('/admin_get_processors', methods=['GET', 'POST'])
def admin_get_processors():
    data = {
        'access_token': session['google_token'],
    }
    # print(session['google_token'])
    groups =jwt.encode( data,  salt, algorithm='HS256', headers={'message': 'OK'})
    r = requests.get("http://127.0.0.1:7000/api/admin_get_processors", data={'data':groups.decode('utf8')})
    r_data = json.loads(r.text)['test'].encode('utf8')
    data = jwt.decode(r_data, salt, algorithms=['HS256'])
    return json.dumps(data)