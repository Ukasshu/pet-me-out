from django import forms
from django.core.validators import RegexValidator


class RegisterForm(forms.Form):
    class MyDateInput(forms.DateInput): #inner class for input type date - otherwise render as text input
        input_type = 'date'
    numeric = RegexValidator(r'^\+?1?\d{9,15}$', "Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    firstName = forms.CharField(label="First name", max_length=30, widget=forms.TextInput(attrs={'placeholder': 'First name'}))
    lastName = forms.CharField(label="Last name", max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Last name'}))
    mail = forms.EmailField(label="Mail", max_length=100, widget=forms.EmailInput(attrs={'placeholder': "Mail address"}))
    city = forms.CharField(label="City", max_length=30, widget=forms.TextInput(attrs={'placeholder': 'City'}))
    contact = forms.CharField(label = "Contact", max_length=16, validators=[numeric], widget=forms.TextInput(attrs={'placeholder': 'Contact'}))
    dateOfBirth = forms.DateField(label="Date of birth", widget=MyDateInput(attrs={'placeholder': 'Date of birth'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}), label="Hasło", max_length=50)


class LogInForm(forms.Form):
    login = forms.EmailField(label="Mail", max_length=100)
    password = forms.CharField(widget=forms.PasswordInput, label="Hasło", max_length=50)
