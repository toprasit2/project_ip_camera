'''
Created on Mar 1, 2013

@author: boatkrap
'''

from . import base

class ProcessorOperating(base.Resource):
    pass


class ProcessorOperatingManager(base.Manager):
    resource_class = ProcessorOperating
    
    def get(self, processor_id):
        return self._get('/processors/%s/operating'%str(processor_id), "processor_operating")
    
    def update(self, processor, action):
        body = dict(
                    processor_operating=dict(action=action)
                    )
        return self._update('/processors/%s/operating'%str(processor.id), "processor_operating", body)