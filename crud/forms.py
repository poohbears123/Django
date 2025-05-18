from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Gender

GENDER_CHOICES = [
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Others', 'Others'),
]

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Gender, Profile

class UserCreateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'required': True}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'required': True}))
    gender = forms.ModelChoiceField(queryset=Gender.objects.all(), required=False, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email'] 

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        username = cleaned_data.get("username")
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")

        if not first_name or not last_name:
            raise ValidationError("Full Name fields (First and Last) are required.")

        if not username:
            self.add_error('username', "Username is required.")

        if not password or not confirm_password:
            self.add_error('password', "Password is required.")
            self.add_error('confirm_password', "Confirm Password is required.")

        if password != confirm_password:
            self.add_error('password', "Password and Confirm Password do not match.")
            self.add_error('confirm_password', "Password and Confirm Password do not match.")
            self.cleaned_data['password'] = ''
            self.cleaned_data['confirm_password'] = ''

        if User.objects.filter(username=username).exists():
            self.add_error('username', "Username already exists.")

        return cleaned_data

class UserUpdateForm(forms.ModelForm):
    gender = forms.ModelChoiceField(queryset=Gender.objects.all(), required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email'] 

    def __init__(self, *args, **kwargs):
        self.user_id = kwargs.pop('user_id', None)
        super().__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exclude(pk=self.user_id).exists():
            raise ValidationError("Username already exists.")
        if not username:
            raise ValidationError("Username is required.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if not first_name or not last_name:
            raise ValidationError("Full Name fields (First and Last) are required.")

        if password or confirm_password:
            if password != confirm_password:
                self.add_error('password', "Password and Confirm Password do not match.")
                self.add_error('confirm_password', "Password and Confirm Password do not match.")
                self.cleaned_data['password'] = ''
                self.cleaned_data['confirm_password'] = ''

        return cleaned_data

class GenderForm(forms.ModelForm):
    class Meta:
        model = Gender
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
        }
