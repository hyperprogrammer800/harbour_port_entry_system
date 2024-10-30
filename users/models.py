from django.db import models
from HEP_system.models import UserFirm
from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image
from master.models import DocumentType, PersonType, EmployeeDesignation, EquipmentType, AccessGate, RateMaster, PortPassIssueCenter
from HEP_system.models import Vehicle, Container

class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, db_column='user_id')
    user_firm = models.ForeignKey(UserFirm, on_delete=models.CASCADE, related_name='persons', db_column='user_firm_id')
    person_type = models.ForeignKey(PersonType, on_delete=models.CASCADE)
    mobile_no = models.CharField(max_length=15, default='12345678')
    email_id = models.EmailField(default='test@123.com')
    reg_date = models.DateField(default=timezone.now)
    reg_no = models.CharField(max_length=50)
    adhaar_no = models.CharField(max_length=14, unique=True)
    designation = models.ForeignKey(EmployeeDesignation, on_delete=models.CASCADE)
    nationality = models.CharField(max_length=50, default='Indian')
    country = models.CharField(max_length=50, default='India')
    dl_expiry = models.DateField(blank=True, null=True, default=timezone.now)
    profile_image = models.ImageField(default='default.jpg' ,upload_to='profile_pics/')
    status = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} Person'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.profile_image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profile_image.path)

class PersonDocument(models.Model):

    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='documents')
    proof_type = models.ForeignKey(DocumentType, on_delete=models.CASCADE)
    id_proof_no = models.CharField(max_length=100, blank=True, null=True)  # Optional
    # document_name = models.CharField(max_length=255)
    document_attach = models.FileField(upload_to='person_documents/')
    upload_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.proof_type} of {self.person.user.username}"


    
class RFIDPass(models.Model):
    rfid_code = models.CharField(max_length=100, unique=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, null=True, blank=True)
    equipment = models.ForeignKey(EquipmentType, on_delete=models.CASCADE, null=True, blank=True)
    container = models.ForeignKey(Container, on_delete=models.CASCADE, null=True, blank=True)
    issued_at = models.DateTimeField(default=timezone.now)
    valid_until = models.DateTimeField(default=timezone.now)
    access_gates = models.ManyToManyField(AccessGate)  # Areas of access
    rate = models.ForeignKey(RateMaster, on_delete=models.CASCADE)  # Link to RateMaster
    request_type = models.CharField(max_length=10, choices=[
        ('online', 'Online'),
        ('offline', 'Offline'),
    ])
    # issue_id = models.ForeignKey(RFIDManagement, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    def __str__(self):
        return f'RFID Pass {self.rfid_code} for {self.person.user.username}'
    
class RFIDManagement(models.Model):
    staff_user = models.ForeignKey(Person, on_delete=models.CASCADE)  # User issuing the RFID pass
    rfid_pass = models.ForeignKey(RFIDPass, on_delete=models.CASCADE, related_name='rfid_managements')
    issue_date = models.DateTimeField(default=timezone.now)
    update_date = models.DateTimeField(default=timezone.now)
    issue_center = models.ForeignKey(PortPassIssueCenter, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)

    def __str__(self):
        return f'RFID Management for {self.rfid_pass.rfid_code} issued by {self.staff_user.user.username}'