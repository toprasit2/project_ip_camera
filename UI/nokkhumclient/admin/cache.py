'''
Created on Mar 2, 2013

@author: boatkrap
'''

from .. import base

class Cache(base.Resource):
    pass
    

class CacheManager(base.Manager):
    resource_class = Cache
    
    def clear(self):
        return self._delete('/admin/cache')
    
    def get(self):
        return self._get('/admin/cache', 'cache')
    