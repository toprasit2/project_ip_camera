'''
Created on Mar 11, 2013

@author: boatkrap
'''

from .. import cameras

class Camera(cameras.Camera):
    @property
    def operating(self):
        return self.manager.api.admin.camera_operating.get(self.id)
        

class CameraManager(cameras.CameraManager):
    resource_class = Camera
    
    def list(self):
        return self._list('/admin/cameras', "cameras")
    
    def get(self, camera_id):
        return self._get('/admin/cameras/%s'%str(camera_id), 'camera')
        