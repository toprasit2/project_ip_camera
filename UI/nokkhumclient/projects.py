'''
Created on Feb 27, 2013

@author: boatkrap
'''

from . import base

class Project(base.Resource):
    
    @property
    def cameras(self):
        return self.manager.api.cameras.list_cameras_by_project(self.id)
    
    @property
    def processors(self):
        return self.manager.api.processors.list_processors_by_project(self.id)
    

class ProjectManager(base.Manager):
    resource_class = Project
    
    def list_user_projects(self, user_id):
        return self._list('/users/%s/projects' % user_id, "projects")
    
    def list(self):
        return self._list('/projects', "projects")
    
    def permissions(self, project_id, user_id):
        return self._list('/projects/%s/permissions/%s' % (project_id, user_id), 'permissions')
    
    def update_permissions(self, project_id, user_id, permission):        
        body = dict(
                permissions=permission
                )
        return self._update('/projects/%s/permissions/%s' % (project_id, user_id), 'permissions', body)
    
    def get(self, project_id):
        return self._get('/projects/%s' % str(project_id), "project")
    
    def get_processors(self, project_id):
        return self._get('/projects/%s/processors' % str(project_id), "processors")
    
    def delete(self, project):
        if type(project) == self.resource_class:
            return self._delete('/projects/%s' % project.id)
        
        return self._delete('/projects/%s' % project)
    
    def add_user(self, project_id, **kwargs):
        body = dict(
                  collaborator=kwargs
                  )
        self._create('/projects/%s/collaboration' % project_id, 'collaborator', body)
    
    def create(self, **kwargs):
        body = dict(
                    project=kwargs
                    )
        return self._create('/projects', 'project', body)
    
    def update(self, project):
        body = dict(
                    project=self.body_builer(project)
                    )
        print("body:", body)
        return self._update('/projects/%s'%project.id , 'project', body)
