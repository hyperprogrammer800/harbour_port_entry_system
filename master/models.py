from django.db import models

# Academic Year
# class AcademicYear(models.Model):
#     from_year = models.PositiveIntegerField()
#     to_year = models.PositiveIntegerField()
#     academic_year = models.CharField(max_length=50)
#     description = models.TextField(blank=True)
#     status = models.BooleanField(default=True)  # Active/Inactive

#     def __str__(self):
#         return self.academic_year

# Port Category
class PortCategory(models.Model):
    category = models.CharField(max_length=100)
    sub_category = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    status = models.BooleanField(default=True)  # Active/Inactive

    def __str__(self):
        return self.category

# Port Area of Access
class PortAreaOfAccess(models.Model):
    area_name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    status = models.BooleanField(default=True)  # Active/Inactive

    def __str__(self):
        return self.area_name

# Port Pass Issue Center
class PortPassIssueCenter(models.Model):
    center_name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    status = models.BooleanField(default=True)  # Active/Inactive

    def __str__(self):
        return self.center_name

# Port Department
class PortDepartment(models.Model):
    department_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    status = models.BooleanField(default=True)  # Active/Inactive

    def __str__(self):
        return self.department_name

# Employee Designation
class EmployeeDesignation(models.Model):
    designation_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    status = models.BooleanField(default=True)  # Active/Inactive

    def __str__(self):
        return self.designation_name

# Company Creation
class Company(models.Model):
    company_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    status = models.BooleanField(default=True)  # Active/Inactive

    def __str__(self):
        return self.company_name

# Purpose of Cargo
class TypesOfCargo(models.Model):
    cargo_type = models.CharField(max_length=100)
    status = models.BooleanField(default=True)  # Active/Inactive

    def __str__(self):
        return self.cargo_type
    
class TypesOfContainer(models.Model):
    container_type = models.CharField(max_length=100)
    status = models.BooleanField(default=True)  # Active/Inactive

    def __str__(self):
        return self.container_type

# Type of Vehicle
class VehicleType(models.Model):
    purpose_of_cargo = models.ForeignKey(TypesOfCargo, on_delete=models.CASCADE)
    vehicle_type = models.CharField(max_length=100)
    vehicle_category = models.CharField(max_length=50, choices=[
        ('Heavy', 'Heavy'),
        ('Light', 'Light'),
    ])
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.vehicle_type} ({self.vehicle_category}) for {self.purpose_of_cargo.cargo_type}"

    
class EquipmentType(models.Model):
    purpose_of_cargo = models.ForeignKey(TypesOfCargo, on_delete=models.CASCADE)
    equipment_type = models.CharField(max_length=100)
    status = models.BooleanField(default=True)  # Active/Inactive

    def __str__(self):
        return f"{self.equipment_type} in {self.purpose_of_cargo.cargo_type}"

# Access Gate Master
class AccessGate(models.Model):
    access_gate = models.CharField(max_length=100)
    short_name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    status = models.BooleanField(default=True)  # Active/Inactive

    def __str__(self):
        return self.access_gate

# Person Type Creation
class PersonType(models.Model):
    person_type = models.CharField(max_length=100)
    status = models.BooleanField(default=True)  # Active/Inactive

    def __str__(self):
        return self.person_type
    
# Rate Master
class RateMaster(models.Model):
    access_gate = access_gate = models.ForeignKey(AccessGate, on_delete=models.CASCADE)
    allowed_type = models.CharField(max_length=50, choices=[('Vehicle', 'Vehicle'), ('Person', 'Person')])
    # type_of_vehicle = models.CharField(max_length=50, choices=[('Light', 'Light'), ('Heavy', 'Heavy'), ('Equipment', 'Equipment')])
    type_of_vehicle = models.ForeignKey(VehicleType, on_delete=models.CASCADE, null=True, blank=True)
    person_type = models.ForeignKey(PersonType, on_delete=models.CASCADE, null=True, blank=True)
    validity = models.CharField(max_length=50, choices=[('Daily', 'Daily'), ('Monthly', 'Monthly'), ('Half Yearly', 'Half Yearly'), ('Yearly', 'Yearly')])
    rate = models.DecimalField(max_digits=10, decimal_places=2)  # Rate in RS

    def __str__(self):
        return f"{self.access_gate.access_gate} per {self.allowed_type} - Rs. {self.rate} {self.validity}"



# Document Master
class DocumentType(models.Model):
    category_type = models.CharField(max_length=50, choices=[('Firm', 'Firm'), ('Users', 'Users'), ('Person', 'Person'), ('Driver', 'Driver'), ('Vehicle', 'Vehicle'), ('Equipment', 'Equipment'), ('Cargo', 'Cargo'), ('Container', 'Container')])
    type_of_proof = models.CharField(max_length=100)
    status = models.BooleanField(default=True)  # Active/Inactive

    def __str__(self):
        return f"{self.category_type} {self.type_of_proof}"

# Pass Validity Penalty
# class PassValidityPenalty(models.Model):
#     rate = models.DecimalField(max_digits=10, decimal_places=2)  # Rate in RS
#     access_gate = models.ForeignKey(AccessGate, on_delete=models.CASCADE)
#     allowed_type = models.CharField(max_length=50, choices=[('Vehicle', 'Vehicle'), ('Person', 'Person')])
#     type_of_vehicle = models.ForeignKey(VehicleType, on_delete=models.CASCADE, null=True, blank=True)
#     person_type = models.ForeignKey(PersonType, on_delete=models.CASCADE, null=True, blank=True)
#     validity = models.CharField(max_length=50, choices=[('Daily', 'Daily'), ('Monthly', 'Monthly'), ('Half Yearly', 'Half Yearly'), ('Yearly', 'Yearly')])
    

#     def __str__(self):
#         return f"{self.access_gate} - {self.allowed_type}"

class PassValidityPenalty(models.Model):
    RATE_CHOICES = [
    ('HEP', 'Harbour Entry Permit'),
    ('Dwell', 'Dwell Time Penalty'),
    ('No Parking', 'No Parking Penalty'),
    ('Cargo Handling', 'Cargo Handling Fee'),
    ('Storage', 'Storage Fee'),
    ('Wharfage', 'Wharfage Fee'),
    ('Demurrage', 'Demurrage Charge'),
    ('Inspection', 'Inspection Fee'),
    ('Pilotage', 'Pilotage Fee'),
    ('Tug Services', 'Tug Services Fee'),
    ('Environmental', 'Environmental Protection Fee'),
    ('Administrative', 'Administrative Fee'),
    ('Customs Clearance', 'Customs Clearance Fee'),
]


    rate = models.DecimalField(max_digits=10, decimal_places=2)  # Rate in RS
    access_gate = models.ForeignKey(AccessGate, on_delete=models.CASCADE)
    allowed_type = models.CharField(max_length=50, choices=[('Vehicle', 'Vehicle'), ('Person', 'Person'), ('Equipment', 'Equipment')])
    type_of_vehicle = models.ForeignKey(VehicleType, on_delete=models.CASCADE, null=True, blank=True)
    person_type = models.ForeignKey(PersonType, on_delete=models.CASCADE, null=True, blank=True)
    validity = models.CharField(max_length=50, choices=[('Daily', 'Daily'), ('Monthly', 'Monthly'), ('Half Yearly', 'Half Yearly'), ('Yearly', 'Yearly')])
    charge_type = models.CharField(max_length=50, choices=RATE_CHOICES, default='Daily')  # Type of charge
    payment_method = models.CharField(max_length=50, default='UPI', choices=[
        ('Credit Card', 'Credit Card'),
        ('Debit Card', 'Debit Card'),
        ('Internet Banking', 'Internet Banking'),
        ('UPI', 'UPI'),
        ('Cash', 'Cash'),
    ])  # Payment methods

    def __str__(self):
        return f"{self.access_gate} - {self.allowed_type} ({self.charge_type})"
