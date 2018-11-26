'''
Created on Mar 6, 2013

@author: boatkrap
'''
from .. import base

from . import users
from . import processor_commands

class ProcessorCommandQueue(base.Resource):
    
    @property
    def processor_command(self):
        return processor_commands.ProcessorCommand(self.manager.api.admin.processor_commands, self._info['processor_command'])
    
class ProcessorCommandQueueManager(base.Manager):
    resource_class = ProcessorCommandQueue
    
    def list(self):
        return self._list('/admin/processor_command_queue', 'processor_command_queue')
    
    def get(self, command_id):
        return self._get('/admin/processor_command_queue/%s'%str(command_id), 'processor_command_queue')