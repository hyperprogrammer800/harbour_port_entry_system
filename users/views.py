from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, PersonUpdateForm, PersonDocumentForm


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
def person(request):
    documents = request.user.person.documents.all()

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = PersonUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.person)
        pd_form = PersonDocumentForm(request.POST,
                                   request.FILES,
                                   instance=request.user.person)
        if u_form.is_valid() and p_form.is_valid() and pd_form.is_valid():
            u_form.save()
            p_form.save()
            pd_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('person')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = PersonUpdateForm(instance=request.user.person)
        pd_form = PersonDocumentForm()

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'pd_form' : pd_form,
        'documents' : documents
    }

    return render(request, 'users/person.html', context)