'''
Created on Mar 2, 2013

@author: boatkrap
'''

from . import base

class Storage(base.Resource):
    def list(self):
        self.manager.list(self.url)
    

class StorageManager(base.Manager):
    resource_class = Storage
    
    
    def list_by_processor(self, processor_id):
        return self._list('/storage/%s'%(processor_id), "files")
    
    def list(self, path):
        if path[-1:] == '/':
            path = path[:-1]
#        print("path: ", path)
        return self._list(path, "files")
    
    def get(self, path):
        if path[-1:] == '/':
            path = path[:-1]
#        print("path sm: ", path)
        return self._get(path, "file")
    
    def delete(self, storage):
        return self._delete(storage.url)
    
    def delete_identify(self, indentify):
        return self._delete(indentify)
    
#    def create(self):
#        pass
#    
#    def update(self):
#        pass