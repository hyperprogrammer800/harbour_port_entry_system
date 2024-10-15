from django.contrib import admin
from . models import Person, PersonDocument, RFIDPass, RFIDManagement

# Register your models here.

admin.site.register([Person, PersonDocument, RFIDPass, RFIDManagement])
