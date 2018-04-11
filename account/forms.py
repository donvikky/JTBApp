from django import forms


class UserRegistrationForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput)
    password = forms.CharField(widget=forms.PasswordInput)
    repeat_password = forms.CharField(widget=forms.PasswordInput)
    email = forms.CharField(widget=forms.EmailInput)
    first_name = forms.CharField()
    last_name = forms.CharField()
