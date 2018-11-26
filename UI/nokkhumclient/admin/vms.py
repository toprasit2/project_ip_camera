'''
Created on Mar 6, 2013

@author: boatkrap
'''
from .. import base
from . import cpu_information
from . import memory_information
from . import disk_information

class VM(base.Resource):
    pass

class VMManager(base.Manager):
    resource_class = VM

    def get(self, compute_node_id):
        return self._get('/admin/compute_nodes/%s/vm'%str(compute_node_id), 'vm')
    