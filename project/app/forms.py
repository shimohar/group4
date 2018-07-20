from django import forms
from app.models import User
from app.models import Material

class LoginForm(forms.Form):
    Userid=forms.CharField(required=True,max_length=16)
    Password=forms.CharField(required=True,max_length=16)

class UserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=('Userid','Password')

class MaterialForm(forms.ModelForm):
    class Meta:
        model=Material
        fields=('name','best_before')