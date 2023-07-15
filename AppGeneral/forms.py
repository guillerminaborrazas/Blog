from django import forms
from django.contrib.auth.forms import UserChangeForm,PasswordChangeForm, UserCreationForm
from django.contrib.auth.models import User
from .models import Blog

class UserEditForm(UserChangeForm):
    username = forms.CharField(widget= forms.TextInput(attrs={"placeholder":"Username"}))
    email = forms.CharField(widget= forms.TextInput(attrs={"placeholder":"Email"}))
    first_name = forms.CharField(widget= forms.TextInput(attrs={"placeholder":"First Name"}))
    last_name = forms.CharField(widget= forms.TextInput(attrs={"placeholder":"Last Name"}))
    password = None

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        help_texts = {k:"" for k in fields}

class formSetBlog(forms.ModelForm):
    pais = forms.CharField(widget= forms.TextInput())
    titulo = forms.CharField(widget= forms.TextInput())
    subtitulo = forms.CharField(widget= forms.TextInput())
    cuerpo = forms.CharField(widget= forms.Textarea())
    #autor = forms.CharField()
    #fecha = forms.DateTimeField()
    imagen = forms.ImageField()

    class Meta:
        model = Blog
        fields = ['pais','titulo', 'subtitulo', 'cuerpo' ,'imagen']
        help_texts = {k:"" for k in fields} 

class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(label = "", widget= forms.PasswordInput(attrs={"placeholder":"Old password"}))
    new_password1 = forms.CharField(label = "", widget= forms.PasswordInput(attrs={"placeholder":"New password"}))
    new_password2 = forms.CharField(label = "", widget= forms.PasswordInput(attrs={"placeholder":"Confirmation new password"}))

    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']
        help_texts = {k:"" for k in fields}

class AvatarForm(forms.Form):
    avatar = forms.ImageField()
