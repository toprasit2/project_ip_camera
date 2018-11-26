'''
Created on Feb 27, 2013

@author: boatkrap
'''
from . import base
from . import roles

class User(base.Resource):
    @property
    def roles(self):
        user_roles = [roles.Role(self.manager.api.roles, r) for r in self._info['roles']]
        return user_roles

class UserManager(base.Manager):
    resource_class = User
    
    def get(self, user_id):
        return self._get('/users/%s'%str(user_id), 'user')