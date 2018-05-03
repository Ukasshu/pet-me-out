from django import forms

class RegisterForm(forms.Form):
    class MyDateInput(forms.DateInput): #inner class for input type date - otherwise render as text input
        input_type = 'date'
    firstName = forms.CharField(label="Imię", max_length=30)
    lastName = forms.CharField(label="Nazwisko", max_length=50)
    mail = forms.EmailField(label="Mail", max_length=100)
    city = forms.CharField(label="Miasto", max_length=30)
    contact = forms.IntegerField(label="Kontakt")
    dateOfBirth = forms.DateField(label="Data urodzenia", widget=MyDateInput)
    password = forms.CharField(widget=forms.PasswordInput, label="Hasło", max_length=50)


class LogInForm(forms.Form):
    login = forms.EmailField(label="Mail", max_length=100)
    password = forms.CharField(widget=forms.PasswordInput, label="Hasło", max_length=50)
