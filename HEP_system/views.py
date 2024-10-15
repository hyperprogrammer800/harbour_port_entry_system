from django.shortcuts import render
from .models import UserFirm
from users.models import Person

# Create your views here.
def home(request):
    context = {
        'title' : 'Home'
    }
    return render(request, 'HEP_system/home.html', context)

def dashboard(request):
    context = {
        'title' : 'Dashboard'
    }
    return render(request, 'HEP_system/dashboard.html', context)

firms = [
    {
        'type' : 'EXPORT',
        'regno' : 'REG23451',
        'name' : 'Santhosh',
        'mobile_no ' : '9876543210',
        'email' : 'Test123@gmail.com'
    },
    {
        'type' : 'IMPORT',
        'regno' : 'REG23452',
        'name' : 'Pandian',
        'mobile_no ' : '9876567890',
        'email' : 'Test321@gmail.com'
    }
]

def user_firm(request):
    context = {
        'firms' : UserFirm.objects.all(),
        'title' : 'User Firms'
    }
    return render(request, 'HEP_system/user_firms/user_firm.html', context)

def user_person(request):
    context = {
        'persons' : Person.objects.all(),
        'title' : 'Person Firms'
    }
    return render(request, 'HEP_system/user_firms/user_person.html', context)