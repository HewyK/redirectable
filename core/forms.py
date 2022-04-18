from django.db.models import fields
from django.forms import ModelForm, Form, widgets
from django import forms
from core.models import *

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username',)

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class UserProfileForm(ModelForm):

    class Meta:
        model = UserProfile
        fields = ('contact_mobile', 'marketing_choice', 'notes',)

        widgets = {
            'contact_mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control'}),
        }


class RedirectsForm(ModelForm):

    url_from = forms.CharField(
        required=True,
        widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'http://example.com'})
    )
    url_to = forms.CharField(
        required=True,
        widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'www.example.com'})
    )
    http_https = forms.ChoiceField(
        required=True,
        choices=HTTP_CHOICES,
        widget = forms.Select(attrs={'class': 'form-control', 'empty_label': 'Please Select'})
        )

    class Meta:
        model = Redirects
        fields = ('url_from', 'url_to', 'http_https',)

