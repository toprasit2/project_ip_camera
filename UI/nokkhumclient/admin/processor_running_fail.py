'''
Created on Mar 6, 2013

@author: boatkrap
'''
from .. import base

from .. import users
from .. import processors
from . import compute_nodes

class ProcessorRunningFail(base.Resource):

    @property
    def processor(self):
        return processors.Processor(self.manager.api.processors, self._info['processor'])
    
    @property
    def compute_node(self):
        if 'compute_node' in self._info:
            return compute_nodes.ComputeNode(self.manager.api.admin.compute_nodes, self._info['compute_node'])
        return None
    

class ProcessorRunningFailManager(base.Manager):
    resource_class = ProcessorRunningFail
    
    def list(self):
        return self._list('/admin/processor_running_fail', 'processor_running_fail')