#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AdminPasswordChangeForm

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


class UserCreateForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_active']    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['is_active'].widget.attrs['class'] = 'active'
        self.fields['username'].required = True
        self.fields['password1'].required = True
        self.fields['password2'].required = True
        self.fields['email'].required = True

class UserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'is_active']   

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['username'].required = True
        self.fields['email'].required = True


class UserPasswordChangeForm(AdminPasswordChangeForm):
    
    class Meta:
        fields = '__all__'


class ZabbixForm(forms.ModelForm):
    
    class Meta:
        model = models.Zabbix
        fields = ['nazev', 'ip_adresa', 'port', 'povolen']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nazev'].widget.attrs['class'] = 'form-control'
        self.fields['ip_adresa'].widget.attrs['class'] = 'form-control'
        self.fields['port'].widget.attrs['class'] = 'form-control'
        self.fields['povolen'].widget.attrs['class'] = 'form-control'
        self.fields['nazev'].required = True