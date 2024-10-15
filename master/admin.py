from django.contrib import admin
from . models import PortCategory, PortAreaOfAccess, PortPassIssueCenter, PortDepartment, EmployeeDesignation, Company, TypesOfCargo,\
      TypesOfContainer, VehicleType, EquipmentType, AccessGate, PersonType,RateMaster, DocumentType, PassValidityPenalty

# Register your models here.

admin.site.register([PortCategory, PortAreaOfAccess, PortPassIssueCenter, PortDepartment, EmployeeDesignation, Company, TypesOfCargo,\
                      TypesOfContainer, VehicleType, EquipmentType, AccessGate, PersonType, RateMaster, DocumentType, PassValidityPenalty])
