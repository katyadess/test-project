from django import forms
from .models import *

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image', 'description']
        
        widgets = {
                'description': forms.TextInput(attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter description'
                }),
            }