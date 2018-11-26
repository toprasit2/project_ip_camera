from . import base
from . import camera_manufactory

class CameraModel(base.Resource):
    
    @property
    def manufactory(self):
        #print("_info: ", self._info)
        return camera_manufactory.CameraManufactory(
                    self.manager.api.camera_manufactories,
                    self._info['manufactory']
                    )

class CameraModelManager(base.Manager):
    resource_class = CameraModel

    def list(self, manufactory_id):
        return self._list('/manufactories/%s/models'%str(manufactory_id), "camera_models")
    
    def get(self, model_id):
        return self._get('/camera_models/%s'%str(model_id), "camera_model")
    