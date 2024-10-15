from django.db import models
from django.utils import timezone
# from django.contrib.auth.models import User
from master.models import VehicleType, TypesOfCargo, TypesOfContainer, DocumentType, EquipmentType
from django.core.exceptions import ValidationError

class UserFirm(models.Model):
    FIRM_TYPE_CHOICES = [
        ('stevedore', 'Stevedore'),
        ('ship_agent', 'Ship Agent'),
        ('custom_broker', 'Custom Broker'),
        ('cfs', 'Container Freight Station'),
        ('freight_forwarder', 'Freight Forwarder'),
        ('terminal_operator', 'Terminal Operator'),
        ('shipping_line', 'Shipping Line'),
        ('warehouse_operator', 'Warehouse Operator'),
        ('transport_carrier', 'Transport Carrier'),
        ('port_authority', 'Port Authority'),
    ]

    name = models.CharField(max_length=255)
    firm_type = models.CharField(max_length=50, choices=FIRM_TYPE_CHOICES)
    phone_no = models.CharField(max_length=15, default='12345677')
    email_id = models.EmailField()
    address_1 = models.CharField(max_length=255)
    address_2 = models.CharField(max_length=255, blank=True, null=True)
    # reg_date = models.DateField(default=timezone.now)
    reg_no = models.CharField(max_length=50)
    contact_person = models.ForeignKey('users.Person', on_delete=models.CASCADE, related_name='userfirm_hep')
    # phone_mobile_no = models.CharField(max_length=15)
    fax_no = models.CharField(max_length=15, blank=True, null=True)
    gstin = models.CharField(max_length=15)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    # login_id = models.CharField(max_length=50, unique=True)
    # password = models.CharField(max_length=128)
    status = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name
    
    def save(self, *args, **kwargs):
        # Check if the firm_type is 'port_authority'
        if self.firm_type == 'port_authority':
            # Check if the user creating this instance is a superuser
            if not self.contact_person.user.is_superuser:
                raise ValidationError("Only superusers can create a UserFirm with type 'port_authority'.")
        
        # Call the parent class's save method
        super().save(*args, **kwargs)
    

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
    # copy_of_rc = models.FileField(upload_to='vehicle_document/')
    # copy_of_fc = models.FileField(upload_to='vehicle_document/')
    # insurance = models.FileField(upload_to='vehicle_document/')
    # puc = models.FileField(upload_to='vehicle_document/')
    # port_approval_letter = models.FileField(upload_to='vehicle_document/')
    # safety_officer_certificate = models.FileField(upload_to='vehicle_document/')
    max_gvm = models.FloatField()
    pollution_control_date = models.DateField()
    fitness_certificate_date = models.DateField()
    insurance_date = models.DateField()
    status = models.BooleanField(default=True)

class Equipment(models.Model):
    equipment_type = models.ForeignKey(EquipmentType, on_delete=models.CASCADE)
    equipment_no = models.CharField(max_length=50)
    firm = models.ForeignKey(UserFirm, on_delete=models.CASCADE, related_name='owned_equipment', default=2)
    reg_date = models.DateField(default=timezone.now)
    reg_no = models.CharField(max_length=50)
    status = models.BooleanField(default=True)

    def __str__(self):
        return f'Equipment {self.equipment_no} owned by {self.firm.name}'

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
    agent_type = models.CharField(max_length=50, choices=UserFirm.FIRM_TYPE_CHOICES)
    agent_details = models.TextField()
    port_of_origin = models.CharField(max_length=255)
    port_of_destination = models.CharField(max_length=255)

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
    agent_type = models.CharField(max_length=50, choices=UserFirm.FIRM_TYPE_CHOICES)
    agent_details = models.TextField()
    port_of_origin = models.CharField(max_length=255)
    port_of_destination = models.CharField(max_length=255)


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
