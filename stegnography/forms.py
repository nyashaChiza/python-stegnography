# myapp/forms.py
from django import forms

class EncodeForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Message to hide'}))
    cover_image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}))


class DecodeForm(forms.Form):
    stego_image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}))
