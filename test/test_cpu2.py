import os
import psutil
import jwt
import httplib2
import json
import requests
import time
salt = 'อิอิอุอิ'

name = "NVR2"
owner = "5810110451@psu.ac.th"
online = "True"

pid = os.getpid()
py = psutil.Process(pid)
while(1):
    data = {
        "name" : name,
        "owner" : owner,
        "online" : online,
        "memory" : {
            "used" : psutil.virtual_memory().used,
            "free" : psutil.virtual_memory().free,
            "total" : psutil.virtual_memory().total
        },
        "disk" : {
            "used" : psutil.disk_usage('/').used,
            "free" : psutil.disk_usage('/').free,
            "total" : psutil.disk_usage('/').total
        },
        "cpu" : {
            "used" : psutil.cpu_percent(interval=1),
            "used_per_cpu" : psutil.cpu_percent(interval=1, percpu=True)
        }
    }
    data =jwt.encode( data,  salt, algorithm='HS256', headers={'message': 'OK'})
    r = requests.put("http://127.0.0.1:7000/api/processors_resource", data={'data':data.decode('utf8')})
    time.sleep(3)