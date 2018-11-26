'''
Created on Sep 12, 2013

@author: boatkrap
'''
from . import base
from . import cameras
from . import image_processors
from . import users
from . import processor_operating


class Processor(base.Resource):

    @property
    def project(self):
        return self.manager.api.projects.get(self._info['project']['id'])

    @property
    def operating(self):
        if 'processor_operating' in self._info:
            return processor_operating.ProcessorOperating(
                self.manager.api.processor_operating,
                self._info['processor_operating']
                )

        return self.manager.api.processor_operating.get(self.id)

    @property
    def storage(self):
        return self.manager.api.storage.list_by_processor(self.id)

    @property
    def cameras(self):
        if 'cameras' in self._info:
            return [cameras.Camera(
                    self.manager.api.cameras,
                    camera) 
                    for camera in self._info['cameras']
                    ]
        return self.manager.api.cameras.list_cameras_by_processor(self.id)

    @cameras.setter
    def cameras(self, cameras):
        self._info['cameras'] = []

        for camera in cameras:
            the_camera = None
            if type(camera) is dict:
                the_camera = camera
            else:
                the_camera = dict(id=camera.id)
            self._info['cameras'].append(
                the_camera
                )

    @property
    def image_processors(self):
        return self._info['image_processors']

    @image_processors.setter
    def image_processors(self, image_processors):
        if 'image_processors' in self._info:
            self._info['image_processors'] = []

        self._info['image_processors'] = image_processors

    @property
    def owner(self):
        return users.User(self.manager.api.users, self._info['owner'])


class ProcessorManager(base.Manager):
    resource_class = Processor

    def list_processors_by_project(self, project_id):
        return self._list('/projects/%s/processors'%str(project_id), 'processors')

    def list(self):
        return self._list('/processors', "processors")

    def get(self, processor_id):
        return self._get('/processors/%s'%str(processor_id), "processor")

    def delete(self, processor_id):
        return self._delete('/processors/%s'%processor_id)

    def create(self, **kwargs):

        body = dict(
            processor=kwargs
            )

        return self._create('/processors', "processor", body)

    def update(self, processor):
        body = dict(
            processor=self.body_builer(processor)
            )

        return self._update('/processors/%s'%processor.id, "processor", body)
