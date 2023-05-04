from django import forms
from .models import *


class DeviceConnect(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['device_ip', 'device_username', 'device_password']
        widgets = {
            'device_ip': forms.TextInput(attrs={
                'class': 'form-control border-1',
                'placeholder': 'IP address',
                'pattern': '^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$',
            }),
            'device_username': forms.TextInput(attrs={
                'class': 'form-control border-1',
                'placeholder': 'Username',
            }),
            'device_password': forms.PasswordInput(attrs={
                'class': 'form-control border-1',
                'placeholder': 'Password',
            })
        }
