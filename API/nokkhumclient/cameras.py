from . import base
from . import camera_manufactory
from . import camera_model
from . import image_processors
from . import users
import json
import datetime


class Camera(base.Resource):

    @property
    def project(self):
        return self.manager.api.projects.get(self._info['project']['id'])

    @property
    def camera_model(self):
        return camera_model.CameraModel(
            self.manager.api.camera_models,
            self._info['model']
            )

    @camera_model.setter
    def camera_model(self, model):
        if 'model' not in self._info:
            self._info['model'] = {}

        self._info['model']['id'] = model.id
        del self._info['model']['manufactory']

    @property
    def owner(self):
        return users.User(self.manager.api.users, self._info['owner'])


class CameraManager(base.Manager):
    resource_class = Camera

    def list_cameras_by_project(self, project_id):
        return self._list('/projects/%s/cameras'
                          % str(project_id),
                          'cameras')

    def list_cameras_by_processor(self, processor_id):
        return self._list('/processors/%s/cameras'
                          % str(processor_id),
                          'cameras')

    def list(self):
        return self._list('/cameras', "cameras")

    def get(self, camera_id):
        return self._get('/cameras/%s'
                         % str(camera_id),
                         "camera")

    def get_camera_by_project(self, camera_id, project_id):
        return self._get('/projects/%s/cameras/%s'
                         % (str(project_id), str(camera_id)),
                         'camera')

    def delete(self, camera):
        return self._delete('/cameras/%s'
                            % camera.id)

    def create(self, **kwargs):
        body = dict(
            camera=kwargs
            )

        return self._create('/cameras',
                            "camera",
                            body)

    def create_by_json(self, camera_json):
        body = json.loads(camera_json)
        return self._create('/cameras',
                            "camera",
                            body)

    def update(self, camera):
        body = dict(
            camera=self.body_builer(camera)
            )
        return self._update('/cameras/%s'
                            % camera.id,
                            "camera",
                            body)
