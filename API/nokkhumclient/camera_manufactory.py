from . import base

class CameraManufactory(base.Resource):

    pass

class CameraManufactoryManager(base.Manager):
    resource_class = CameraManufactory
    
    def list(self):
        return self._list('/manufactories', "manufactories")
    
    def get(self, manufactory_id):
        return self._get('/manufactories/%s'%str(manufactory_id), "manufactory")
    