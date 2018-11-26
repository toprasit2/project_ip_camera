'''
Created on Feb 5, 2014

@author: wongpiti
'''
from . import base

import datetime

class ServicePlan(base.Resource):
    pass

class ServicePlanManager(base.Manager):
    resource_class = ServicePlan
    
    
    def get(self, service_plan_id):
        return self._get('/billing/service_plans/%s'%str(service_plan_id), "service_plan")
    
    def list(self):
        return self._list('/billing/service_plans', "service_plans")
    
    def create(self, **kwargs):
        body = dict(
                    service_plan=kwargs
                    )
        return self._create('/billing/service_plans', 'service_plan', body)
        
    def delete(self, service_plan):
        return self._delete('/billing/service_plans/%s'%str(service_plan.id))
    
    
    
    
    
    