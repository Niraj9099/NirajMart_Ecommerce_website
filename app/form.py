from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import password_validation
from .models import Customer


# ---------- User ragistration Form -------------

class UserragistrationForm(UserCreationForm):
    password1 = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Conform password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    email = forms.CharField(required=True , widget=forms.EmailInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'first_name','last_name', 'email', 'password1', 'password2']
        labels = {'email': 'Email'}
        widgets = {'username': forms.TextInput(attrs={'class':'form-control'}),
                   'first_name' : forms.TextInput(attrs={'class':'form-control'}),
                   'last_name' : forms.TextInput(attrs={'class':'form-control'}),
                }


# ---------------------- User Login Form ---------------------------

class UserLoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={"autofocus": True, 'class':'form-control'}))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password",  'class':'form-control'}),
    )
    class Meta:
        model = User
        fields = ['username', 'password']


# ---------------------- User Change Password Form ---------------------------

class UserChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", "autofocus": True, 'class':'form-control'}
        ),
    )
    new_password1 = forms.CharField(
        label=_("New password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'class':'form-control'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'class':'form-control'}),
    )


# ---------------------- mypassword Reset ---------------------------

class mypasswordReset(PasswordResetForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email", 'class':'form-control'}),
    )

# ---------------------- mypassword Conform ---------------------------

class mypasswordConform(SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'class':'form-control'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'class':'form-control'}),
    )

# ---------------------- Create CustomerForm ---------------------------

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'village', 'city', 'pincode', 'state']
        widgets = {
            'name' : forms.TextInput(attrs={'class':'form-control'}),
            'village' : forms.TextInput(attrs={'class':'form-control'}),
            'city' : forms.TextInput(attrs={'class':'form-control'}),
            'pincode' : forms.NumberInput(attrs={'class':'form-control'}),
            'state' :  forms.TextInput(attrs={'class':'form-control'}),

        }