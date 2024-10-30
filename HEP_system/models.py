from django.db import models
from django.utils import timezone
# from django.contrib.auth.models import User
from master.models import VehicleType, TypesOfCargo, TypesOfContainer, DocumentType, EquipmentType, UserFirmType
from django.core.exceptions import ValidationError

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

class UserFirm(models.Model):
    name = models.CharField(max_length=255)
    user_firm_type = models.ForeignKey(UserFirmType, on_delete=models.CASCADE, related_name='user_firms')
    phone_no = models.CharField(max_length=15)
    email_id = models.EmailField()
    address_1 = models.CharField(max_length=255)
    address_2 = models.CharField(max_length=255, blank=True, null=True)
    reg_no = models.CharField(max_length=50)
    created_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_user', default=1)
    fax_no = models.CharField(max_length=15, blank=True, null=True)
    gstin = models.CharField(max_length=15)
    website = models.URLField(blank=True, null=True)
    registration_date = models.DateField(blank=True, null=True, default=timezone.now)
    license_number = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    status = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name
    
    def save(self, *args, **kwargs):
        # Check if the user type is 'Port Authority'
        if self.user_firm_type.type_name == 'Port Authority':
            # Check if the user creating this instance is a superuser
            if not self.created_user.is_superuser:
                raise ValidationError("Only superusers can create a UserFirm with type 'Port Authority'.")
        
        # Call the parent class's save method
        super().save(*args, **kwargs)

class Equipment(models.Model):
    equipment_type = models.ForeignKey(EquipmentType, on_delete=models.CASCADE)
    equipment_no = models.CharField(max_length=50)
    firm = models.ForeignKey(UserFirm, on_delete=models.CASCADE, related_name='owned_equipment', default=2)
    reg_date = models.DateField(default=timezone.now)
    reg_no = models.CharField(max_length=50)
    status = models.BooleanField(default=True)

    def __str__(self):
        return f'Equipment {self.equipment_no} of {self.firm.name}'

class Cargo(models.Model):
    name_of_cargo = models.CharField(max_length=255)
    importer_exporter_name = models.CharField(max_length=255)
    import_export_no = models.CharField(max_length=50)  # Fetch from Port API
    cargo_type = models.ForeignKey(TypesOfCargo, on_delete=models.CASCADE)
    firm = models.ForeignKey(UserFirm, on_delete=models.CASCADE, related_name='owned_cargos', default=2)
    
    address = models.CharField(max_length=255)
    contact_no = models.CharField(max_length=15)
    
    no_of_packages = models.IntegerField()
    total_weight = models.FloatField()
    vessel_serial_no = models.CharField(max_length=50)
    vessel_name = models.CharField(max_length=255)
    agent_type = models.ForeignKey(UserFirmType, on_delete=models.CASCADE, default=5)
    agent_details = models.TextField()
    port_of_origin = models.CharField(max_length=255)
    port_of_destination = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name_of_cargo} of {self.firm.name}'

class Container(models.Model):
    name_of_container = models.CharField(max_length=255)
    importer_exporter_name = models.CharField(max_length=255)
    import_export_no = models.CharField(max_length=50)  # Fetch from Port API
    container_type = models.ForeignKey(TypesOfContainer, on_delete=models.CASCADE)
    firm = models.ForeignKey(UserFirm, on_delete=models.CASCADE, related_name='owned_cointainer', default=2)
    address = models.CharField(max_length=255)
    contact_no = models.CharField(max_length=15)
    no_of_packages = models.IntegerField()
    total_weight = models.FloatField()
    vessel_serial_no = models.CharField(max_length=50)
    vessel_name = models.CharField(max_length=255)
    agent_type = models.ForeignKey(UserFirmType, on_delete=models.CASCADE, default=8)
    agent_details = models.TextField()
    port_of_origin = models.CharField(max_length=255)
    port_of_destination = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name_of_container} of {self.firm.name}'    

class Vehicle(models.Model):
    VEHICLE_TYPE = [
        ('small', 'Small'),
        ('large', 'Large'),
        ('heavy', 'Heavy')
    ]
    vehicle_no = models.CharField(max_length=50)
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.CASCADE)
    firm = models.ForeignKey(UserFirm, on_delete=models.CASCADE, related_name='owned_vehicles', default=2)
    reg_date = models.DateField(default=timezone.now)
    reg_no = models.CharField(max_length=50)
    max_gvm = models.FloatField()
    pollution_control_date = models.DateField()
    fitness_certificate_date = models.DateField()
    insurance_date = models.DateField()
    status = models.BooleanField(default=True)

    def __str__(self):
        return f'Vehicle no - {self.vehicle_no} of {self.firm.name}'
    # copy_of_rc = models.FileField(upload_to='vehicle_document/')
    # copy_of_fc = models.FileField(upload_to='vehicle_document/')
    # insurance = models.FileField(upload_to='vehicle_document/')
    # puc = models.FileField(upload_to='vehicle_document/')
    # port_approval_letter = models.FileField(upload_to='vehicle_document/')
    # safety_officer_certificate = models.FileField(upload_to='vehicle_document/')


class VehicleDocument(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='vehicle_documents')
    proof_type = models.ForeignKey(DocumentType, on_delete=models.CASCADE)
    document_attach = models.FileField(upload_to='vehicle_documents/')
    upload_date = models.DateField(default=timezone.now)

class EquipmentDocument(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='equipment_documents')
    proof_type = models.ForeignKey(DocumentType, on_delete=models.CASCADE)
    document_attach = models.FileField(upload_to='equipment_documents/')
    upload_date = models.DateField(default=timezone.now)


class CargoDocument(models.Model):
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE, related_name='cargo_documents')
    proof_type = models.ForeignKey(DocumentType, on_delete=models.CASCADE)
    document_attach = models.FileField(upload_to='cargo_documents/')
    upload_date = models.DateField(default=timezone.now)

class ContainerDocument(models.Model):
    container = models.ForeignKey(Container, on_delete=models.CASCADE, related_name='container_documents')
    proof_type = models.ForeignKey(DocumentType, on_delete=models.CASCADE)
    document_attach = models.FileField(upload_to='container_documents/')
    upload_date = models.DateField(default=timezone.now)


# Online web based HEP request, generation and issuance system model

#material and visitors models needed to be implemented

# class PersonLogin(models.Model):
#     user_firm = models.ForeignKey(UserFirm, on_delete=models.CASCADE)
#     username = models.CharField(max_length=50, unique=True)
#     password = models.CharField(max_length=128)
#     captcha = models.CharField(max_length=6)

# class FirmUserLogin(models.Model):
#     user_firm = models.ForeignKey(UserFirm, on_delete=models.CASCADE)
#     login_id = models.CharField(max_length=50)
#     password = models.CharField(max_length=128)
