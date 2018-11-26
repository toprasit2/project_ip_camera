from .. import base

class CPUInformation(base.Resource):
    pass

class CPUInformationManager(base.Manager):
    resource_class = CPUInformation
    
    