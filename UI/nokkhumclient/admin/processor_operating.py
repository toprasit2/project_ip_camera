'''
Created on Mar 1, 2013

@author: boatkrap
'''

from .. import processor_operating
from . import compute_nodes
class ProcessorOperating(processor_operating.ProcessorOperating):

    @property
    def compute_node(self):
        if 'compute_node' in self._info:
            return compute_nodes.ComputeNode(self.manager.api.admin.compute_nodes, self._info['compute_node'])
        return None


class ProcessorOperatingManager(processor_operating.ProcessorOperatingManager):
    resource_class = ProcessorOperating

    def get(self, processor_id):
        return self._get('/admin/processors/%s/operating'%str(processor_id), "processor_operating")

    def update(self, processor, action):
        body = dict(
                    processor_operating=dict(action=action)
                    )
        return self._update('/admin/processors/%s/operating'%str(processor.id), "processor_operating", body)
