'''
Created on Nov 29, 2013

@author: wongpiti
'''
from . import base

import datetime

class BillingCycle(base.Resource):
    pass

class BillingCycleManager(base.Manager):
    resource_class = BillingCycle
    
    
    def list(self, processor_id):
        return self._list('/billing/processors/%s/cycle'%(str(processor_id)), "billing_cycle")