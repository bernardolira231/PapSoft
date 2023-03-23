from django import forms
from .models import *


class DeviceConnect(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['device_ip', 'device_username', 'device_password']
        widgets = {
            'device_ip': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'IP address',
            }),
            'device_username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username',
            }),
            'device_password': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Password',
            })
        }
