from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, PersonUpdateForm, PersonDocumentForm, PersonCreateForm, PermissionForm, RoleCreationForm, UserRolesForm, PermissionFormDefault
from users.models import Person
from django.contrib.auth.models import User, Permission, Group
from django.urls import reverse
# Create your views here.

def register(request):
    if request.method == 'POST':
        u_form = UserRegisterForm(request.POST)
        p_form = PersonCreateForm(request.POST, request.FILES)
        if u_form.is_valid() and p_form.is_valid():
                user = u_form.save()
                person = p_form.save(commit=False)
                person.user = user
                print(type(p_form.cleaned_data['user_firm']),p_form.cleaned_data['user_firm'],"USER FIRM ID")
                person.user_firm = p_form.cleaned_data['user_firm']  # Set user_firm here
                person.save()

                username = u_form.cleaned_data.get('username')
                messages.success(request, f'Person has been created! {username} are now able to log in')
                return redirect('app-person-register', person_id=user.id)
    else:
        u_form = UserRegisterForm()
        p_form = PersonCreateForm()
    return render(request, 'users/register.html', {'u_form': u_form, 'p_form' : p_form})

@login_required
def person_list(request):
    context = {
        'persons' : Person.objects.all(),
        'title' : 'Person Firms'
    }
    return render(request, 'users/person_list.html', context)


@login_required
def person_register(request, person_id=None):
    # documents = request.user.person.documents.all()
    if person_id:
        print(person_id,"PERSON IDDD")
        selected_user = User.objects.get(id=int(person_id))
    else:
        selected_user = request.user

    pd_form = PersonDocumentForm()
    documents = None
    if Person.objects.filter(user=selected_user).exists():
        documents = selected_user.person.documents.all()

    if request.method == 'POST':
        if 'create_person' in request.POST:
            print(request.POST,"create person POST PAY")
            u_form = UserRegisterForm(request.POST)
            p_form = PersonCreateForm(request.POST, request.FILES)
            selected_user = None
            documents = None
            if u_form.is_valid() and p_form.is_valid():
                user = u_form.save()
                person = p_form.save(commit=False)
                person.user = user
                print(type(p_form.cleaned_data['user_firm']),p_form.cleaned_data['user_firm'],"USER FIRM ID")
                person.user_firm = p_form.cleaned_data['user_firm']  # Set user_firm here
                person.save()

                username = u_form.cleaned_data.get('username')
                messages.success(request, f'Person has been created! {username} are now able to log in')
                return redirect('app-person-register', person_id=user.id)
            else:
                messages.error(request, "There were errors in your submission. Please correct them.")
        if 'update_person' in request.POST:
            u_form = UserUpdateForm(request.POST, instance=selected_user)
            p_form = PersonUpdateForm(request.POST,
                                    request.FILES,
                                    instance=selected_user.person)
            
            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                messages.success(request, f'Your account Person information has been updated!')
                return redirect('app-person-register')
        if 'upload_document' in request.POST:
            pd_form = PersonDocumentForm(request.POST, request.FILES)  # No instance needed
            if pd_form.is_valid():
                print(selected_user.username,"SELECTED USERNAME")
                document = pd_form.save(commit=False)  # Create the instance but don’t save yet
                document.person = selected_user.person  # Associate the document with the person
                document.save()  # Now save it
                messages.success(request, 'Your document has been uploaded!')
                if person_id:
                    return redirect('app-person-register', person_id=selected_user.person.id)
                else:
                    return redirect('app-person-register')
                
            else:
                messages.error(request, 'There was an error uploading the document.')
    else:
        print(request.GET, "request details")
        if 'create' == request.GET.get('action', ''):
            u_form = UserRegisterForm()
            p_form = PersonCreateForm()
            selected_user = None
            documents = None
        else:
            u_form = UserUpdateForm(instance=selected_user)
            if Person.objects.filter(user=selected_user).exists():
                p_form = PersonUpdateForm(instance=selected_user.person)
            else:
                selected_user = None
                p_form = PersonCreateForm()
            

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'pd_form' : pd_form,
        'selected_user' : selected_user,
        'documents' : documents
    }

    return render(request, 'users/person_register.html', context)


@login_required
def permission_management(request, user_id=None):

    selected_user = request.POST.get('user') if request.method == 'POST' else user_id if user_id else None
    print("selected_user---->",request.POST.get('user'), request.method,user_id)
    users_option = Person.objects.filter(user_firm__user_firm_type_id=1)
    
    if selected_user:
        selected_user = User.objects.get(id=selected_user)
        print("SELECTED --->",selected_user,request.GET,selected_user.is_staff)
    if request.method == 'POST' and selected_user and request.POST.get('action') == 'save':
        
        form = PermissionForm(request.POST, is_staff=selected_user.is_staff, user=selected_user)

        if form.is_valid():
            print("VALIDATIONS")
            for perm in Permission.objects.all():
                if perm.codename in form.cleaned_data and form.cleaned_data.get(perm.codename):
                    print("ADDING", perm)
                    selected_user.user_permissions.add(perm)
                else:
                    print("REMOVING", perm)
                    selected_user.user_permissions.remove(perm)

            selected_user.save()  # Save user to persist changes
            form = PermissionForm(request.POST, is_staff=selected_user.is_staff, user=selected_user)
            return redirect('permission_management_with_user', user_id= f'{selected_user.id}')  # Replace with your success URL
    else:
        if selected_user:
            form = PermissionForm(is_staff=selected_user.is_staff, user=selected_user)
        else:
            form = PermissionForm(is_staff=None, user=None)
    # form = PermissionFormDefault(request)
    return render(request, 'groups/permission.html', {
        'title': 'Permission Management',
        'form': form,
        'selected_user': selected_user,
        'users' : users_option
    })

@login_required
def group_role_creation(request, role_id=None):
    roles = Group.objects.all()
    if request.method == 'POST':
        form = RoleCreationForm(request.POST)
        if form.is_valid():
            group = form.save()
            return redirect('roles-creation', role_id=group.id)

    else:
        if role_id:
            role_obj = Group.objects.get(id=role_id)
            initial_data = {'role_name': role_obj.name}
            
            # Include current permissions
            for perm in Permission.objects.all():
                initial_data[perm.codename] = perm in role_obj.permissions.all()

            form = RoleCreationForm(initial=initial_data)
        else:
            form = RoleCreationForm()

    context = {
        'form' : form,
        'title' : 'Role Creation',
        'roles' : roles
    }
    return render(request,'groups/roles_creation.html', context)

@login_required
def assign_user_role(request):
    users = User.objects.filter(person__status=True)
    user_id = request.GET.get('user_id', None)
    print(user_id, "Got USER ID")
    
    if user_id:
        # Initialize the form with the user_id
        form = UserRolesForm(request.POST or None, user_id=user_id)
        
        if request.method == 'POST':
            if form.is_valid():
                user = get_object_or_404(User, id=user_id)
                form.save(user)  # Save the roles for the user
                # Redirect to a success page or back to the roles assignment page
                return redirect(f'{reverse("assign-role")}?user_id={user_id}')
    else:
        form = UserRolesForm()  # Empty form if no user_id is provided

    return render(request, 'groups/roles_assign.html', {
        'users': users,
        'form': form,
        'title': 'User Role Assign'
    })