import os
import secrets
from flask import  render_template, url_for, flash, redirect, request, abort, session, jsonify, Markup
from camera import app, bcrypt, google, cache
from camera.forms import RegistrationForm, LoginForm, GroupOfCamerasForm, CamerasForm, ComputeForm
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
    print(resp)
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
            flash(f'welcome '+name, 'green lighten-2')
        return redirect(url_for('cameras'))

@cache.cached(timeout=50)
@app.route('/cameras')
def cameras():
    if 'google_token' in session:
        user = get_user()
        if user == 'error':
            return redirect(url_for('logout'))
        groups = get_groups()
        camera_status = {
            'active': 'active'
        }
        # composite_list = [cameras[x:x+2] for x in range(0, len(cameras),2)]
        # for i in composite_list:
        #     print(i)
        return render_template('cameras_all.html', title="Camearas", groups=groups, camera_status=camera_status, user=user)
    return render_template('cameras_all.html', title="Camearas")

@cache.cached(timeout=50)
@app.route('/cameras/<group_id>/<display>')
def camera(group_id, display):
    if 'google_token' in session:
        user = get_user()
        if user == 'error':
            return redirect(url_for('logout'))
        groups = get_groups()
        # print(groups)
        group = get_group(group_id)
        camera_status = {
            'active': 'active'
        }
        return render_template('cameras_in_group.html', title="Camera", user=user, camera_status=camera_status, groups=groups, group=group, display=display)
    return redirect(url_for('index'))

@cache.cached(timeout=50)
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
            flash(f'{cameras["name"]} added', 'green lighten-2')
            return redirect(back)
        return render_template("add_camera.html", title="Add Camera", form=form, user=user,back=back,group_name=group_name)


@cache.cached(timeout=50)
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
        flash(f'Group {groups["group_name"]} added', 'green lighten-2')
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
            print(data)
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
    flash(f'{group_name} has deleted', 'green lighten-2')
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
            print(cameras)
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
    flash(f'{camera_name} has deleted', 'green lighten-2')
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
        print(data)
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
        flash(f'Group {form.name.data} added', 'green lighten-2')
        return redirect(back)
    return render_template('add_compute.html', title="Cameras", form=form, user=user, back=back)


@app.route('/get_processors', methods=['GET', 'POST'])
def get_processors():
    data = {
        'access_token': session['google_token'],
    }
    print(session['google_token'])
    groups =jwt.encode( data,  salt, algorithm='HS256', headers={'message': 'OK'})
    r = requests.get("http://127.0.0.1:7000/api/processors", data={'data':groups.decode('utf8')})
    r_data = json.loads(r.text)['test'].encode('utf8')
    data = jwt.decode(r_data, salt, algorithms=['HS256'])
    return json.dumps(data)
