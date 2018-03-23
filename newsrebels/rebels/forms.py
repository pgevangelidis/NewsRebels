from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
#from rebels.models import UserProfile

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), help_text='Your Password *')
    first = forms.CharField(max_length=30, required=False, help_text='Your First Name *')
    last = forms.CharField(max_length=30, required=False, help_text='Your Last Name *')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password')
