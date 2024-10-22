from django.contrib import admin
from . models import UserFirm, Vehicle, Cargo, Container, VehicleDocument, CargoDocument, ContainerDocument, Equipment, EquipmentDocument

# Register your models here.

admin.site.register([UserFirm, Vehicle, Cargo, Container, VehicleDocument, CargoDocument, ContainerDocument, Equipment, EquipmentDocument])
