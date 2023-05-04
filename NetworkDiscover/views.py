from django.shortcuts import render, redirect
from .models import *
from .forms import *
from netmiko import ConnectHandler, exceptions

# Create your views here.


def index(request):
    return render(request, 'index.html')


def start(request):

    if request.method == 'GET':
        return render(request, 'start.html', {
            'form': DeviceConnect
        })
    else:
        try:
            l_device = []
            ssh_user = request.POST['device_username']
            ssh_password = request.POST['device_password']
            device_ip = request.POST['device_ip']
            device = {
                'device_type': 'cisco_ios',
                'host': device_ip,
                'username': ssh_user,
                'password': ssh_password
            }
            device_list = []

            known_ip = []

            known_ip.append(device_ip)

            for i in known_ip:
                device['host'] = i
                ip_disp = []
                add_neighbors = []

                net_connect = ConnectHandler(**device)

                output = net_connect.send_command(
                    'show cdp neighbors detail', use_textfsm=True)
                output1 = net_connect.send_command(
                    'show ip interface brief', use_textfsm=True)
                output2 = net_connect.send_command(
                    'show running-config | include hostname')
                output3 = net_connect.send_command(
                    'show ip interface brief', use_textfsm=True)
                net_connect.disconnect()

                hostname = ''
                for f in range(len(output2)):
                    while f >= 9 and f <= len(output2):
                        hostname += output2[f]
                        break

                cont_int = (len(output3))

                if cont_int >= 10:
                    output3 = 'Switch'
                else:
                    output3 = 'Router'
                deviceType = output3

                for x in output:
                    if x['management_ip'] not in known_ip:
                        if device_ip[0:3] in x['management_ip']:
                            known_ip.append(x['management_ip'])

                for each in output1:
                    if each['status'] == 'up':
                        ip_disp.append(each['ipaddr'])

                l_device.append(
                    {
                        'name': hostname,
                        'type': deviceType,
                        'ip': i,
                    }
                )

            new_list = []
            names_list = []

            for cada in range(len(device_list)):
                for cado in range(len(device_list)):
                    if cada == cado:
                        break
                    if device_list[cada]['name'] != device_list[cado]['name']:
                        new_list.append(device_list[cado])
                        names_list.append(device_list[cado]['name'])

            for leach in new_list:
                device2 = Device.objects.create(
                    device_username=request.POST['device_username'],
                    device_password=request.POST['device_password'],
                    device_ip=leach['ip'],
                    device_name=leach['name'],
                    device_type=leach['type']
                )
                device2.save()

            return redirect('/show_device', net_connect, new_list)
        except Exception as e:
            return render(request, 'start.html', {
                'form': DeviceConnect,
                'error': 'La conexion no se ha encontrado'
            })


def show_device(request, net_connect, l):
    disp = Device.objects.all()
    return render(request, 'show_device.html', {
        'device': disp
    })
