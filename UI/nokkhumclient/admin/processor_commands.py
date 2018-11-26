'''
Created on Mar 6, 2013

@author: boatkrap
'''
from .. import processor_commands
from . import users
from . import processors
from . import compute_nodes

class ProcessorCommand(processor_commands.ProcessorCommand):
    @property
    def processor(self):
        if self._info['processor'] is None:
            return None
        
        return processors.Processor(self.manager.api.admin.processors, self._info['processor'])
    
    @property
    def owner(self):
        if 'owner' not in self._info:
            return None
        
        if self._info['owner'] is None:
            return None
        
        return users.User(self.manager.api.admin.users, self._info['owner'])
    
    @property
    def compute_node(self):
        if 'compute_node' not in self._info:
            return None
        
        if self._info['compute_node'] is None:
            return None
        
        return compute_nodes.ComputeNode(self.manager.api.admin.compute_nodes, self._info['compute_node'])

class ProcessorCommandManager(processor_commands.ProcessorCommandManager):
    resource_class = ProcessorCommand
    
    def list(self):
        return self._list('/admin/processor_commands', 'processor_commands')
    
    def get(self, processor_command_id):
        return self._get('/admin/processor_commands/%s'%str(processor_command_id), 'processor_command')