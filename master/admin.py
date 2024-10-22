from django.contrib import admin
from .models import AccessGate, Company, DocumentType, EmployeeDesignation, PortAreaOfAccess, PortCategory, PortDepartment, PortPassIssueCenter, PassValidityPenalty, RateMaster, TypesOfCargo, TypesOfContainer, VehicleType, PersonType

# Register your models here.
admin.site.register([
    AccessGate,
    Company,
    DocumentType,
    EmployeeDesignation,
    PassValidityPenalty,
    PortAreaOfAccess,
    PortCategory,
    PortDepartment,
    PortPassIssueCenter,
    RateMaster,
    TypesOfCargo,
    TypesOfContainer,
    VehicleType,
    PersonType,
])

