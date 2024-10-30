from typing import Any, Mapping
from django.contrib.auth.forms import UserCreationForm
from django.forms.renderers import BaseRenderer
from django.forms.utils import ErrorList
from . models import Person, PersonDocument
from django import forms
from django.contrib.auth.models import User, Permission, Group

class RoleCreationForm(forms.Form):
    role_name = forms.CharField(max_length=100, required=True, label="Role Name")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        permissions = Permission.objects.all()
        for permission in permissions:
            initial = False
            self.fields[permission.codename] = forms.BooleanField(
                    required=False,
                    label=permission.name,
                    initial=initial
            )
    def save(self):
        role_name = self.cleaned_data['role_name']
        group, created = Group.objects.get_or_create(name=role_name)
        print(group.permissions.all(),"GROUP RECEIVED")
        for perm in Permission.objects.all():
            if perm in group.permissions.all():
                group.permissions.remove(perm)
            if self.cleaned_data.get(perm.codename):
                group.permissions.add(perm)
        
        group.save()
        return group
    
class UserRolesForm(forms.Form):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user_id', None)
        super().__init__(*args, **kwargs)
        roles = Group.objects.all()
        user_roles = []
        if user:
            user_roles = User.objects.get(id=int(user)).groups.all()
        for role in roles:
            initial = role in user_roles
            self.fields[role.name] = forms.BooleanField(
                    required=False,
                    label=role.name,
                    initial=initial
            )
    def save(self, user):
        # Clear existing groups
        user.groups.clear()

        # Add groups based on form data
        for role, is_checked in self.cleaned_data.items():
            if is_checked:
                group, created = Group.objects.get_or_create(name=role)
                user.groups.add(group)
    
class PermissionForm(forms.Form):
    # user = forms.ModelChoiceField(queryset=User.objects.all(), required=True)

    def __init__(self, *args, **kwargs):
        is_staff = kwargs.pop('is_staff', False)
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.initialize_permission_fields(user, is_staff)

    def initialize_permission_fields(self, user, is_staff):
        permissions = Permission.objects.all()
        user_permissions = []
        if user:
            user_permissions = [perm.codename for perm in user.user_permissions.all()]
            print(f"User: {user.username}, Permissions: {[perm.codename for perm in user.user_permissions.all()]}")
        for permission in permissions:
            if permission.content_type.app_label == 'auth' and user:
                # initial = user.has_perm(permission.codename) if user else None
                initial = True if permission.codename in user_permissions else False
                self.fields[permission.codename] = forms.BooleanField(
                    required=False,
                    label=permission.name,
                    initial=initial
                )
            elif permission.content_type.app_label == 'users' and user:  # Replace with your app label
                if 'delete' not in permission.codename:
                    # initial = user.has_perm(permission.codename) if user else None
                    initial = True if permission.codename in user_permissions else False
                    self.fields[permission.codename] = forms.BooleanField(
                        required=False,
                        label=permission.name,
                        initial=initial
                    )

class PermissionFormDefault(forms.Form):
    class Meta:
        model = Permission
        fields = ['__all__']





class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['email']

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