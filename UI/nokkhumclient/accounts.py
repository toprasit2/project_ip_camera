from . import base

class Account(base.Resource):
    def list_projects(self):
        return self.api.projects.list_user_projects(self.id)

class AccountManager(base.Manager):
    
    resource_class = Account
    
    def register(self, **kwargs):
        body = dict(
                    user=kwargs
                    )
        self._create('/accounts', 'user', body)