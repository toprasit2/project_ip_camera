'''
Created on Feb 5, 2014

@author: wongpiti
'''
from .. import base
from .. import service_plan

import datetime

class DefaultServicePlan(base.Resource):
    pass

class DefaultServicePlanManager(base.Manager):
    resource_class = service_plan.ServicePlan
    
    
#     def get(self, service_plan_id):
#         return self._get('/billing/service_plans/%s'%str(service_plan_id), "service_plan")
#     
#     def list(self):
#         return self._list('/billing/service_plans', "service_plans")
    
    def set_default(self, service_plan_id):
        return self._create('/billing/service_plans/%s/default'%service_plan_id, 'service_plan', None)
        
#     def delete(self, service_plan):
#         return self._delete('/billing/service_plans/%s'%str(service_plan.id))
