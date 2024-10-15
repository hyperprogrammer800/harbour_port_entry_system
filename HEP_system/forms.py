from django import forms
from .models import VehicleDocument, CargoDocument, ContainerDocument

class VehicleDocumentForm(forms.ModelForm):
    class Meta:
        model = VehicleDocument
        fields = ['proof_type', 'document_attach']

class CargoDocumentForm(forms.ModelForm):
    class Meta:
        model = CargoDocument
        fields = ['proof_type', 'document_attach']

class ContainerDocumentForm(forms.ModelForm):
    class Meta:
        model = ContainerDocument
        fields = ['proof_type', 'document_attach']
