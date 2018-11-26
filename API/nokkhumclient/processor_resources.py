'''
Created on Nov 29, 2013

@author: wongpiti
'''
from . import base

import datetime

class ProcessorResource(base.Resource):
    pass

class ProcessorResourceManager(base.Manager):
    resource_class = ProcessorResource
    
    
    def get(self, processor_id, start_date, end_date, operation='MAX'):
        return self._get('/user_resources/%s?start_date=%s&end_date=%s&operation=%s'%(str(processor_id), start_date, end_date, operation), "processor_resource")