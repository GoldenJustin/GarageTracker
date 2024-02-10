from django import forms
from .models import Owner

class OwnerRegistrationForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = ['owner_code', 'email', 'password', 'first_name', 'middle_name', 'last_name', 'gender', 'avatar']
        widgets = {'password': forms.PasswordInput()}

class OwnerLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())