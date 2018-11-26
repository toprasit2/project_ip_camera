'''
Created on Nov 29, 2013

@author: wongpiti
'''
from .. import billing

import datetime

class Billing(billing.Billing):
    pass

class BillingManager(billing.BillingManager):
    resource_class = Billing
    
    
    def get(self, processor_id, start_date, end_date, operation='MAX', user_id=None, service_plan_id=None):
        url = '/billing/processors/%s?start_date=%s&end_date=%s&operation=%s'%(str(processor_id), start_date, end_date, operation)
        if service_plan_id is not None:
            url = '/billing/processors/%s?start_date=%s&end_date=%s&operation=%s&service_plan=%s'%(str(processor_id), start_date, end_date, operation, service_plan_id)
        if user_id is not None:
            url += "&user_id=%s"%user_id
        return self._get(url, "processor_billing")