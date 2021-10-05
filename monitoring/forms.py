#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate

from . import models

class PrihlaseniForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = self.cleaned_data
        username = cleaned_data['username']
        heslo = cleaned_data['password']
        user = authenticate(username=username, password=heslo)
        if user is not None:
            return cleaned_data 
        else:
            text = _("Nesprávné jméno nebo heslo")
            self.add_error('username', text)
            raise forms.ValidationError(text)


class GatewayForm(forms.ModelForm):
    
    class Meta:
        model = models.Gateway
        fields = ['nazev', 'eui', 'povolena']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nazev'].widget.attrs['class'] = 'form-control'
        self.fields['eui'].widget.attrs['class'] = 'form-control'
        self.fields['povolena'].widget.attrs['class'] = 'form-control'
        self.fields['nazev'].required = True
        self.fields['eui'].required = True


class ZarizeniForm(forms.ModelForm):
    
    class Meta:
        model = models.Zarizeni
        fields = ['nazev', 'devaddr', 'deveui', 'nwkskey', 'appskey', 'povoleno']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nazev'].widget.attrs['class'] = 'form-control'
        self.fields['devaddr'].widget.attrs['class'] = 'form-control'
        self.fields['deveui'].widget.attrs['class'] = 'form-control'
        self.fields['nwkskey'].widget.attrs['class'] = 'form-control'
        self.fields['appskey'].widget.attrs['class'] = 'form-control'
        self.fields['povoleno'].widget.attrs['class'] = 'form-control'
        self.fields['nazev'].required = True
        self.fields['devaddr'].required = True
        self.fields['deveui'].required = True
        self.fields['nwkskey'].required = True
        self.fields['appskey'].required = True