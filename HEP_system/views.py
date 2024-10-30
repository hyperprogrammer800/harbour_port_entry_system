from django.shortcuts import render
from HEP_system.models import UserFirm, Vehicle, Container, Cargo, Equipment
from users.models import Person, RFIDPass

# Create your views here.
def home(request):
    context = {
        'title' : 'Home'
    }
    return render(request, 'HEP_system/home.html', context)

def dashboard(request):
    # Count instances of each model
    user_firm_count = UserFirm.objects.count()
    active_user_firm_count = UserFirm.objects.filter(status=True).count()
    
    person_count = Person.objects.count()
    active_person_count = Person.objects.filter(status=True).count()

    vehicle_count = Vehicle.objects.count()
    active_vehicle_count = Vehicle.objects.filter(status=True).count()

    container_count = Container.objects.count()
    # active_container_count = Container.objects.filter(status=True).count()
    active_container_count = 0
    
    cargo_count = Cargo.objects.count()
    # active_cargo_count = Cargo.objects.filter(status=True).count()
    active_cargo_count = 0

    equipment_count = Equipment.objects.count()
    active_equipment_count = Equipment.objects.filter(status=True).count()

    rfid_pass_count = RFIDPass.objects.count()
    active_rfid_pass_count = RFIDPass.objects.filter(status=True).count()

    context = {
        'title': 'Dashboard',
        'user_firms': f"{active_user_firm_count} / {user_firm_count}",
        'persons': f"{active_person_count} / {person_count}",
        'vehicles': f"{active_vehicle_count} / {vehicle_count}",
        'containers': f"{active_container_count} / {container_count}",
        'cargos': f"{active_cargo_count} / {cargo_count}",
        'equipments': f"{active_equipment_count} / {equipment_count}",
        'rfid_passes': f"{active_rfid_pass_count} / {rfid_pass_count}",
    }
    return render(request, 'HEP_system/dashboard.html', context)


def user_firm(request):
    context = {
        'firms' : UserFirm.objects.all(),
        'title' : 'User Firms'
    }
    return render(request, 'HEP_system/user_firms/user_firm.html', context)

def user_person(request):
    pass
