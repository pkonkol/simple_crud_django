from django import forms

from .models import Email, Osoba, Telefon


class OsobaForm(forms.ModelForm):
    class Meta:
        model = Osoba
        fields = ['id', 'imie', 'nazwisko']
        widgets = {'id': forms.HiddenInput()}


class TelefonForm(forms.ModelForm):
    class Meta:
        model = Telefon
        fields = ['telefon']


class EmailForm(forms.ModelForm):
    class Meta:
        model = Email
        fields = ['email']
