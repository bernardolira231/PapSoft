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

            output = net_connect.send_command('show inventory')

            for line in output.splitlines():
                if 'Chassis' in line:
                    if 'router' in line.lower():
                        sor = 'router'
                    elif 'switch' in line.lower():
                        sor = 'switch'
                    else:
                        sor = 'desconocido'
                    break
            else:
                sor = 'desconocido'

            output = net_connect.send_command('show run | i hostname')
            hostname = output.split()[1]

            device = Device.objects.create(
                device_username=request.POST['device_username'],
                device_password=request.POST['device_password'],
                device_ip=request.POST['device_ip'],
                device_type=sor,
                device_name=hostname,
            )
            device.save()

            output = net_connect.send_command('show cdp neighbors detail')
            for line in output.splitlines():
                if 'IP address: ' in line:
                    new_ip_address = line.split('IP address: ')[1]

            return redirect('/show_device', net_connect)
        except:
            return render(request, 'start.html', {
                'form': form,
                'error': 'La conexion no se ha encontrado'
            })


def show_device(request, net_connect):
    return render(request, 'show_device.html')
