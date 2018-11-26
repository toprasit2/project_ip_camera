'''
Created on Feb 27, 2013

@author: boatkrap
'''
from . import base

class Role(base.Resource):
    pass

class RoleManager(base.Manager):
    resource_class = Role
    