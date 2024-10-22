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


def user_firm(request):
    context = {
        'firms' : UserFirm.objects.all(),
        'title' : 'User Firms'
    }
    return render(request, 'HEP_system/user_firms/user_firm.html', context)

def user_person(request):
    pass
