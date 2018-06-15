from django import forms
from django.core.validators import RegexValidator

PET_TYPE_CHOICES = (
    ("DOG", "Dog"),
    ("CAT", "Cat"),
    ("HAMSTER", "Hamster"),
    ("BIRD", "Bird"),
    ("OTHER", "Other")
)


class RegisterForm(forms.Form):
    class MyDateInput(forms.DateInput):  # inner class for input type date - otherwise render as text input
        input_type = 'date'

    numeric = RegexValidator(r'^\+?1?\d{9,15}$',
                             "Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    firstName = forms.CharField(label="", max_length=30,
                                widget=forms.TextInput(attrs={'placeholder': 'First name', 'class': 'form-control'}))
    lastName = forms.CharField(label="", max_length=50,
                               widget=forms.TextInput(attrs={'placeholder': 'Last name', 'class': 'form-control'}))
    mail = forms.EmailField(label="", max_length=100,
                            widget=forms.EmailInput(attrs={'placeholder': "Mail address", 'class': 'form-control'}))
    city = forms.CharField(label="", max_length=30,
                           widget=forms.TextInput(attrs={'placeholder': 'City', 'class': 'form-control'}))
    contact = forms.CharField(label="", max_length=16, validators=[numeric],
                              widget=forms.TextInput(attrs={'placeholder': 'Contact', 'class': 'form-control'}))
    dateOfBirth = forms.DateField(label="",
                                  widget=MyDateInput(attrs={'placeholder': 'Date of birth', 'class': 'form-control'}))
    username = forms.CharField(label="", max_length=20,
                               widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}),
                               label="", max_length=50)


class LogInForm(forms.Form):
    username = forms.CharField(label="", max_length=20,
                               widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}),
                               label="", max_length=50)


class ImageUploadForm(forms.Form):
    image = forms.ImageField()


class AddPetForm(forms.Form):
    name = forms.CharField(label="", max_length=30)
    weight = forms.FloatField(min_value=0)
    height = forms.FloatField(min_value=0)
    type = forms.ChoiceField(choices=PET_TYPE_CHOICES)
