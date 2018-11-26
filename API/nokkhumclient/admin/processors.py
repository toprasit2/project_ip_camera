'''
Created on Mar 1, 2013

@author: boatkrap
'''

from .. import processors
from . import compute_nodes
from . import processor_operating
import urllib

from .. import base


class Resource(base.Resource):
    pass


class ResourceManager(base.Manager):
    resource_class = Resource

    def list(self, resource_id):
        return self._list('/admin/processors/%s/resources'
                          % str(resource_id),
                          'resources')


class Processor(processors.Processor):

    @property
    def compute_node(self):
        if 'compute_node' in self._info:
            return compute_nodes.ComputeNode(self.manager.api.admin.compute_nodes, self._info['compute_node'])
        return None

    @property
    def operating(self):
        if 'processor_operating' in self._info:
            return processor_operating.ProcessorOperating(
                self.manager.api.processor_operating,
                self._info['processor_operating']
                )

        return self.manager.api.processor_operating.get(self.id)


class ProcessorManager(processors.ProcessorManager):
    resource_class = Processor

    def list(self, **kws):
        url = '/admin/processors'
        if len(kws) > 0:
            parameters = urllib.parse.urlencode(kws)
            url += '?'+parameters
        return self._list(url, "processors")

    def get(self, processor_id):
        return self._get('/admin/processors/%s' % str(processor_id), "processor")

    def update(self, processor):
        body = dict(
            processor=self.body_builer(processor)
        )

        return self._update('/admin/processors/%s'%str(processor.id), "processor", body)

    def get_resources(self, processor_id):
        return ResourceManager(self.api).list(processor_id)

