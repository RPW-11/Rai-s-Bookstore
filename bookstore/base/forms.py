from django import forms
from django.forms import ModelForm, NumberInput
from .models import Book

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-field'}),
            'author': forms.TextInput(attrs={'class':'form-field'}),
            'publisher': forms.TextInput(attrs={'class':'form-field'}),
            'isbn': forms.TextInput(attrs={'class':'form-field'}),
            'itemWeight': forms.NumberInput(attrs={'class':'form-field'}),
            'dimension': forms.TextInput(attrs={'class':'form-field'}),
            'pages': forms.NumberInput(attrs={'class':'form-field'}),
            'language': forms.TextInput(attrs={'class':'form-field'}),
            'ratings': forms.NumberInput(attrs={'class':'form-field'}),
        }