import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core import validators


class SignupForm(UserCreationForm):
    username = forms.CharField(
        max_length=30,
        required=True,
        strip=True,
        validators=[
            validators.RegexValidator(
                regex=r'^[a-zA-Z0-9]*$',
                message="Username must contain at least one alphabet character.",
            ),
        ],
    )
    email = forms.EmailField(required=True)
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput,
        required=True,
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput,
        required=True,
    )

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")

        # Check if password contains at least one uppercase letter.
        if not any(char.isupper() for char in password1):
            raise forms.ValidationError("Password must contain at least one uppercase letter.")

        # Check if password contains at least one digit.
        if not any(char.isdigit() for char in password1):
            raise forms.ValidationError("Password must contain at least one digit.")

        # Check if password contains at least one non-alphanumeric character.
        if not re.search(r'[!@#$%^&*()_+]', password1):
            raise forms.ValidationError("Password must contain at least one special character.")

        return password1

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match. Please enter the same password in both fields.")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
