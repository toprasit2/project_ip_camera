'''
Created on Nov 29, 2013

@author: wongpiti
'''
from . import base

import datetime

class Billing(base.Resource):
    pass

class BillingManager(base.Manager):
    resource_class = Billing
    
    
    def get(self, processor_id, start_date, end_date, operation='MAX'):
        return self._get('/billing/processors/%s?start_date=%s&end_date=%s&operation=%s'%(str(processor_id), start_date, end_date, operation), "processor_billing")