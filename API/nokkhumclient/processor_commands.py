'''
Created on Mar 6, 2013

@author: boatkrap
'''
from . import base
from . import users
from . import processors

class ProcessorCommand(base.Resource):
    @property
    def processor(self):
        return processors.Processor(self.manager.api.processors, self._info['processor'])
    
    @property
    def owner(self):
        return users.User(self.manager.api.users, self._info['owner'])

class ProcessorCommandManager(base.Manager):
    resource_class = ProcessorCommand
    
    def list(self):
        return self._list('/admin/processor_commands', 'processor_commands')
    
    def get(self, processor_command_id):
        return self._get('/admin/processor_commands/%s'%str(processor_command_id), 'processor_command')