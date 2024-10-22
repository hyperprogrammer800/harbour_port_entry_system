from django import forms
from django.apps import apps
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404


def model_info(request):
    if request.user.is_authenticated and (request.user.is_superuser or request.user.is_staff):
        models = []
        apps_names = ['master','HEP_system']
        formatted_results = {}
        for app in apps_names:
            app_config = apps.get_app_config(app)  # Replace with your app name
            for model in app_config.get_models():
                if 'Document' in model.__name__ and not model.__name__.split('Document')[-1]:
                    continue
                models.append(model.__name__)

            formatted_models = {}
            for model in models:
                current_word = ""
                split_names = []
                for char in model:
                    if char.isupper() and current_word:
                        split_names.append(current_word)
                        current_word = char
                    else:
                        current_word += char
                if current_word:
                    split_names.append(current_word)
            
                formatted_models[model] = ' '.join(split_names)
            formatted_results[f'formatted_{app}_models'] = formatted_models
            models = []
        return formatted_results
    return {}




def dynamic_model_list_view(request, app_name, model_name):
    # Check if the user is authenticated and has appropriate permissions
    if not request.user.is_authenticated or not (request.user.is_superuser or request.user.is_staff):
        raise Http404("Unauthorized access")

    # Get the model class dynamically
    try:
        model_class = apps.get_model(app_name, model_name.capitalize())
    except LookupError:
        raise Http404("Model not found")
    # print(model_class.objects.all()[0].__dict__,"RECEIVED OBJECT OF",model_name.capitalize())
    # Fetch all objects from the model
    objects = model_class.objects.all()
    fields = [field for field in model_class._meta.get_fields() if not field.auto_created] # if not field.is_relation and
    
    # Get formatted model names
    formatted_models = model_info(request)
    formatted_model_name = formatted_models[f'formatted_{app_name}_models'].get(model_name, None)
    print('FORMATTED MODELS ---> ',formatted_model_name)
    
    return render(request, 'HEP_system/settings/dynamic_model_list.html', {
        'app_name' : app_name,
        'model_name': model_name,
        'formatted_model_name': formatted_model_name,
        'objects': objects,
        'fields': fields,
    })

def dynamic_model_register(request, app_name, model_name, id=None):
    if not request.user.is_authenticated or not (request.user.is_superuser or request.user.is_staff):
        raise Http404("Unauthorized access")

    # Get the model class dynamically
    try:
        model_class = apps.get_model(app_name, model_name.capitalize())
        print("FORM CREATION MODEL NAME --->",model_class.__name__)
    except LookupError:
        raise Http404("Model not found")

    # Create a ModelForm for the model
    ModelForm = forms.modelform_factory(model_class, exclude=[])

    if id is not None:
        instance = get_object_or_404(model_class, id=id)
    else:
        instance = None

    if request.method == 'POST':
        form = ModelForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('app-dynamic-model', app_name=app_name, model_name=model_name)
    else:
        form = ModelForm(instance=instance)

    return render(request, 'HEP_system/settings/dynamic_model_creation.html', {
        'app_name' : app_name,
        'model_name' : model_name,
        'form': form,
        'model_name': model_name,
    })