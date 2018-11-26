'''
Created on Dec 5, 2012

@author: superizer
'''
import requests
import json

from . import accounts
from . import cameras
from . import processors
from . import processor_commands
from . import processor_operating
from . import camera_manufactory
from . import camera_model
from . import projects
from . import storage
from . import image_processors
from . import users
from . import roles
from . import admin
from . import groups
from . import notification
from . import billing
from . import billing_cycle
from . import processor_resources
from . import service_plan


class HTTPClient:
    def __init__(self, username, password,
                 host, port=80,
                 secure_connection=False,
                 token=None):

        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.secure_connection = secure_connection
        self.auth_token = token
        self.user_id = None

        self.scheme = "http"
        if self.secure_connection:
            self.scheme = "https"

        self.api_url = '%s://%s:%d' % (self.scheme, self.host, self.port)

    def authenticate(self):
        body = {'password_credentials': {'password': self.password,
                                         'username': self.username}}

        response = self.request(self.api_url + '/authentication/tokens',
                                "POST",
                                body=body,
                                headers={})
        if response:
            self.auth_token = response['access']['token']['id']
            self.user_id = response['access']['user']['id']
            return response
        return None

    def request(self, url, method, **kwargs):
        kwargs['headers']['Content-Type'] = 'application/json'

        if 'body' in kwargs:
            kwargs['data'] = json.dumps(kwargs['body'])
            del kwargs['body']

        print(method, url, "\nargs:", kwargs)
        response = requests.request(method, 
                                    url,
                                    **kwargs)

        if response.status_code == 200:
            print("response:", response.json())
            return response.json()
        else:
            print("response.status_code:", response.status_code)
            if response.status_code == "403":
                raise "403 Forbidden"

        return None

    def _cs_request(self, url, method, **kwargs):
        if self.auth_token is None:
            self.authenticate()

        kwargs.setdefault('headers', {})['X-Auth-Token'] = self.auth_token

        return self.request(self.api_url + url, 
                            method,
                            **kwargs)

    def get(self, url, **kwargs):
        return self._cs_request(url, 'GET', **kwargs)

    def post(self, url, **kwargs):
        return self._cs_request(url, 'POST', **kwargs)

    def put(self, url, **kwargs):
        return self._cs_request(url, 'PUT', **kwargs)

    def delete(self, url, **kwargs):
        return self._cs_request(url, 'DELETE', **kwargs)


class Client:
    def __init__(self, username, password,
                 host="127.0.0.1", port=80,
                 secure_connection=False,
                 token=None):

        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.secure_connection = secure_connection

        self.http_client = HTTPClient(username,
                                      password,
                                      host,
                                      port,
                                      secure_connection,
                                      token
                                      )

        self.accounts = accounts.AccountManager(self)
        self.cameras = cameras.CameraManager(self)
        self.projects = projects.ProjectManager(self)
        self.storage = storage.StorageManager(self)
        self.camera_models = camera_model.CameraModelManager(self)
        self.camera_manufactories = camera_manufactory.CameraManufactoryManager(self)
        self.image_processors = image_processors.ImageProcessorManager(self)
        self.users = users.UserManager(self)
        self.roles = roles.RoleManager(self)
        self.processors = processors.ProcessorManager(self)
        self.processor_operating = processor_operating.ProcessorOperatingManager(self)
        self.processor_commands = processor_commands.ProcessorCommandManager(self)

        self.groups = groups.GroupManager(self)
        self.notification = notification.NotificationManager(self)

        self.processor_resources = processor_resources.ProcessorResourceManager(self)
        self.billing = billing.BillingManager(self)
        self.billing_cycle = billing_cycle.BillingCycleManager(self)
        self.service_plans = service_plan.ServicePlanManager(self)
        # admin
        self.admin = admin.AdministratorClient(self)

    def authenticate(self):
        return self.http_client.authenticate()
