from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from myapp.models import Center


class LoginForm(AuthenticationForm):
    pass


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class CreateCenterForm(forms.ModelForm):
    class Meta:
        model = Center
        fields = ('center_name', 'start_hour', 'start_minute', 'end_hour', 'end_minute')
    # center_name = forms.CharField(max_length=100)
    # start_hour = forms.IntegerField(label='Start Hour')
    # start_minute = forms.IntegerField(label='Start Minute')
    # end_hour = forms.IntegerField(label='End Hour')
    # end_minute = forms.IntegerField(label='End Minute')
