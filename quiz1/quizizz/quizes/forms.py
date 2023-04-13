# forms.py

from django import forms
from captcha.fields import ReCaptchaField

class ContactForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    email = forms.EmailField(label='Email', max_length=100)
    message = forms.CharField(label='Message', widget=forms.Textarea)
    captcha = ReCaptchaField()
