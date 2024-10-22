from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, PersonUpdateForm, PersonDocumentForm, PersonCreateForm
from users.models import Person
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from HEP_system.models import UserFirm
# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! {username} are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

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