from django import forms
from django.apps import apps
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.db import models
from django.core.paginator import Paginator

def model_info(request):
    if request.user.is_authenticated and (request.user.is_superuser or request.user.is_staff):
        models = []
        apps_names = ['master','HEP_system', 'users']
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
    # print("ALL FIELDS --->",  model_class._meta.get_fields())
    fields = [field for field in model_class._meta.get_fields() if not field.auto_created] # if not field.is_relation and

    filter_options = {
        'date_fields': [],
        'choice_fields': [],
        'text_fields': [],
        'foreign_key_fields': {},
    }

    filter_criteria = {}

    for field in fields:
        if isinstance(field, models.DateField):
            filter_options['date_fields'].append(field.name)

            from_date = request.GET.get(f'{field.name}_from')
            to_date = request.GET.get(f'{field.name}_to')
            if from_date:
                filter_criteria[f"{field.name}__gte"] = from_date
            if to_date:
                filter_criteria[f"{field.name}__lte"] = to_date
        elif isinstance(field, models.CharField) or isinstance(field, models.TextField):
            filter_options['text_fields'].append(field.name)

            text_value = request.GET.get(field.name)
            if text_value:
                filter_criteria[f"{field.name}__icontains"] = text_value
        elif field.choices:
            filter_options['choice_fields'].append((field.name, field.choices))

            selected_value = request.GET.get(field.name)
            if selected_value:
                filter_criteria[f"{field.name}"] = selected_value
        elif isinstance(field, models.ForeignKey):
            # Get the related model and its display names
            related_model = field.related_model
            related_objects = related_model.objects.all()
            filter_options['foreign_key_fields'][field.name] = [(obj.id, str(obj)) for obj in related_objects]

            selected_fk_value = request.GET.get(field.name)
            if selected_fk_value:
                filter_criteria[f"{field.name}"] = selected_fk_value
            

    # Apply filters if there are any criteria
    if filter_criteria:
        objects = model_class.objects.filter(**filter_criteria)
    else:
        objects = model_class.objects.all()
    
    current_page=1
    if request.GET.get('page', None):
        print('PAGINATION--->', request.GET.get('page'))
        current_page = int(request.GET.get('page'))
    paginator = Paginator(objects, 10)
    page_obj = paginator.get_page(current_page)
    
    # Get formatted model names
    formatted_models = model_info(request)
    formatted_model_name = formatted_models[f'formatted_{app_name}_models'].get(model_name, None)
    
    return render(request, 'HEP_system/settings/dynamic_model_list.html', {
        'app_name' : app_name,
        'model_name': model_name,
        'formatted_model_name': formatted_model_name,
        'objects': page_obj,
        'total_pages_range' : range(1,1+paginator.num_pages),
        'total_pages' : paginator.num_pages,
        'current_page' : current_page,
        'fields': fields,
        'filter_options' : filter_options
    })

    # all_fields = model_class._meta.get_fields()
    # field_info = []
    # for field in all_fields:
    #     if not field.auto_created:
    #         field_info.append({
    #             'name': field.name,
    #             'type': field.get_internal_type(),  # Get the field type
    #             'verbose_name': field.verbose_name,
    #             'is_relation': field.is_relation
    #         })
    # print('FIELD INFO ---> ',field_info)



def dynamic_model_register(request, app_name, model_name, id=None):
    if not request.user.is_authenticated or not (request.user.is_superuser or request.user.is_staff):
        if not request.user.has_perm('users.add_rfidpass') and model_name == 'RFIDPass':
            raise Http404("Unauthorized access due to restricted RFIDPass model role")
        if not model_name == 'RFIDPass':
            raise Http404("Unauthorized access")
    # Get the model class dynamically
    try:
        model_class = apps.get_model(app_name, model_name.capitalize())
        print(model_name,"FORM CREATION MODEL NAME --->",model_class.__name__)
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