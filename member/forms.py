import re
from django import forms
from django.contrib.auth.models import User
from member.models import UserProfile
from django.core.exceptions import ValidationError

class RegisterForm(forms.Form):
    username = forms.CharField(label='ID', max_length=32)
    password = forms.CharField( label='Password', widget=forms.PasswordInput(render_value=False) )
    password_confirm = forms.CharField( label='Password Confirm', widget=forms.PasswordInput(render_value=False) )
    email = forms.EmailField(label='Email')
    nickname = forms.CharField(label='Nickname', max_length=32)

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
            raise ValidationError('Already used ID.')
        except User.DoesNotExist:
            return username

    def clean_password_confirm(self):
        if not self.cleaned_data.has_key('password') or self.cleaned_data['password'] != self.cleaned_data['password_confirm']:
            raise ValidationError("Password is not matched.");
        return self.cleaned_data


    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.get(email = email)
            raise ValidationError('Already used Email.')
        except User.DoesNotExist:
            return email

    def clean_nickname(self):
        nickname = self.cleaned_data['nickname']
        try:
            User.objects.get(first_name=nickname)
            raise ValidationError('Already used Nickname.')
        except User.DoesNotExist:
            return nickname

class LoginForm(forms.Form):
    username = forms.CharField(label='ID')
    password = forms.CharField(label='Password', widget=forms.PasswordInput(render_value=False))

    def clean(self):
        try:
            user = authenticate(username=self.cleaned_data['username'], password=self.cleaned_data['password'])
            if user:
                self._user = user
            else:
                raise ValidationError('Password is wrong.')
        except User.DoesNotExit:
            raise ValidationError('That ID is not exist.')
        return self.cleaned_data
    
    def get_user(self):
        return self._user
