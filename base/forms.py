from django.forms import ModelForm
from .models import Room, User
from django.contrib.auth.forms import UserCreationForm
from django import forms


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'e.g. example123@abc.com'}))
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'e.g. sahruz_riyad'}),
            'password1': forms.PasswordInput(attrs={'placeholder': '••••••••'}),
            'password2': forms.PasswordInput(attrs={'placeholder': '••••••••'}),
        }
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user