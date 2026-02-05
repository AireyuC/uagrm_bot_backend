from django import forms

class StudentLoginForm(forms.Form):
    registro = forms.CharField(label="Registro Universitario", max_length=20, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 2150...'}))
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '******'}))
    phone = forms.CharField(widget=forms.HiddenInput()) # El teléfono viene oculto en la URL
