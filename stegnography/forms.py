# myapp/forms.py
from django import forms

class TextEncodeForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Message to hide'}))
    cover_image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}))

class FileEncodeForm(forms.Form):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    cover_image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}))

class TextDecodeForm(forms.Form):
    stego_image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}))


class FileDecodeForm(forms.Form):
    stego_image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}))
