'''
Created on Jan 15, 2014

@author: yoschanin.s
'''

from . import base

class Notification(base.Resource):
    
    @property
    def cameras(self):
        return self.manager.api.cameras.list_cameras_by_project(self.id)
    
    @property
    def processors(self):
        return self.manager.api.processors.list_processors_by_project(self.id)
    

class NotificationManager(base.Manager):
    resource_class = Notification

    def get(self):
        return self._get('/notifications', 'notifications')
    
    def read(self, json):
        body = dict(
                  notifications=json
                  )
        self.api.http_client.post('/notifications', body=body)
