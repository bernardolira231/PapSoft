from django.shortcuts import render, redirect
from .models import *
from .forms import *
from netmiko import ConnectHandler, exceptions
# import networkx as nx

# Create your views here.


def index(request):
    return render(request, 'index.html')


def start(request):
    form = DeviceConnect
    if request.method == 'GET':
        return render(request, 'start.html', {
            'form': form
        })
    else:
        try:
            ssh_user = request.POST['device_username']
            ssh_password = request.POST['device_password']
            device_ip = request.POST['device_ip']
            device = {
                'device_type': 'cisco_ios',
                'host': device_ip,
                'username': ssh_user,
                'password': ssh_password
            }
            net_connect = ConnectHandler(**device)
            return redirect('/show_device', net_connect)
        except:
            return render(request, 'start.html', {
                'form': form,
                'error': 'La conexion no se ha encontrado'
            })


def show_device(request, net_connect):
    return render(request, 'show_device.html')
