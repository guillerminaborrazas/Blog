from django import forms

class formNewMessage(forms.Form):
    contenido = forms.CharField(widget= forms.TextInput())