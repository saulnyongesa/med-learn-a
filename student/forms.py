from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy

from student.models import *


class PWDChangeView(PasswordChangeView):
    form = PasswordChangeForm
    success_url = reverse_lazy('signout-url')


class UserDetailsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'phone', 'email']

    def __init__(self, *args, **kwargs):
        super(UserDetailsForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.disabled = True


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'phone', 'email']

class UserProfileImageEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['profile_image']


class UserSignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'phone',
            'email',
        ]
