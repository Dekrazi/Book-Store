from django import forms
from django.contrib.auth.models import User, Group


class UserGroupForm(forms.Form):
    user = forms.ModelChoiceField(
        queryset=User.objects.all(), empty_label="Select a user"
    )
    group = forms.ModelChoiceField(
        queryset=Group.objects.all(), empty_label="Select a group"
    )
