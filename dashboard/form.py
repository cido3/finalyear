from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(
        label='',  # Remove the label
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Enter your username'
        })
    )
    password = forms.CharField(
        label='',  # Remove the label
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Enter your password'
        })
    )
    remember_me = forms.BooleanField(
        required=False,
        label='',  # Remove the label
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )
