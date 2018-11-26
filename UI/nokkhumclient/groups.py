'''
Created on Dec 28, 2013

@author: yoschanin.s
'''

from . import base

class Group(base.Resource):
    
    @property
    def cameras(self):
        return self.manager.api.cameras.list_cameras_by_project(self.id)
    
    @property
    def processors(self):
        return self.manager.api.processors.list_processors_by_project(self.id)
    

class GroupManager(base.Manager):
    resource_class = Group
    
    def list_user_projects(self, user_id):
        return self._list('/users/%s/projects'%user_id, "projects")
    
    def list_processor(self, group_id):
        return self._get('/groups/%s/processors'%group_id, "group")
    
    def get(self, group_id):
        return self._get('/groups/%s'%str(group_id), "group")
    
    def delete(self, project):
        return self._delete('/projects/%s'%project.id)
    
    def add_user(self, groupid, userid):
        body=dict(
                  collaborator=dict(
                                    id=userid
                                    )
                  )
        self._create('/groups/%s/collaborators'%groupid,'collaborator', body)
    def create(self, **kwargs):
        body = dict(
                    group=kwargs
                    )
        self._create('/groups', 'group', body)
        
    def new_topic(self, **kwargs):
        body = dict(
                    topic=kwargs
                    )
        self.api.http_client.post('/forums', body=body)
    
    def get_forum(self, group_id):
        return self._list('/forums/%s'%str(group_id), "forums")
    
    def update(self):
        pass