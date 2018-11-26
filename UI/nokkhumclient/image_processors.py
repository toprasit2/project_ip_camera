'''
Created on Mar 6, 2013

@author: boatkrap
'''

from . import base

class ImageProcessor(base.Resource):
    pass
    

class ImageProcessorManager(base.Manager):
    resource_class = ImageProcessor
    
    def list(self):
        return self._list('/image_processors', "image_processors")