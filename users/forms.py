from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from . models import Person, PersonDocument


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class PersonDocumentForm(forms.ModelForm):
    class Meta:
        model = PersonDocument
        fields = ['proof_type', 'document_attach']

class PersonCreateForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = [
            'user_firm', 
            'person_type', 
            'mobile_no', 
            'email_id', 
            'reg_no', 
            'adhaar_no', 
            'designation', 
            'nationality', 
            'country', 
            'dl_expiry', 
            'profile_image'
        ]


class PersonUpdateForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['user_firm', 'person_type', 'designation', 'nationality', 'country', 'adhaar_no',  'profile_image', 'dl_expiry', 'mobile_no', 'email_id']