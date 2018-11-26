'''
Created on Feb 27, 2013

@author: boatkrap
'''
from .. import users

class User(users.User):
    pass

class UserManager(users.UserManager):
    resource_class = User
    
    def list(self):
        return self._list('/admin/users', 'users')
    
    def get(self, user_id):
        return self._get('/admin/users/%s'%str(user_id), 'user')