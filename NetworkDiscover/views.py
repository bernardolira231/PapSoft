from django.shortcuts import render, redirect
from .models import *
from .forms import *
from netmiko import ConnectHandler, exceptions
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import os
# Create your views here.


def index(request):
    return render(request, 'index.html')


def start(request):

    if request.method == 'GET':
        # si la informacion entra por metodo get se renderiza la pagina web con el formulario
        return render(request, 'start.html', {
            'form': DeviceConnect
        })
    else:
        # si la informacion entra por metodo post se realiza el proceso de conexion
        try:  # Se hace un try para poder observar si no se da ninguna excepcion
            l_device = []
            l_neighbors = []
            # se guarda la informacion
            ssh_user = request.POST['device_username']
            # que se ingresa en el form
            ssh_password = request.POST['device_password']
            # recuperandose por el metodo POST
            device_ip = request.POST['device_ip']
            Device.objects.all().delete()
            # os.remove("/NetworkDiscover/static/img/Graph.png")
            # print(device_ip)
            device = {
                'device_type': 'cisco_ios',
                'host': device_ip,
                'username': ssh_user,
                'password': ssh_password
            }  # Se ingresa la informacion a un diccionario para la posterior connexión
            known_ip = []

            # Se agrega la ip ingresada por el usuario a la lista de ip's conocidas
            known_ip.append(device_ip)

            # Se inicia un ciclo con todas las ip's conocidas
            for i in known_ip:
                # Se le ingresa la ip que esta en la iteracion actual al diccionario anterior
                device['host'] = i
                ip_disp = []
                add_neighbors = []

                # Se hace la connexión con ayuda de la libreria de netmiko
                net_connect = ConnectHandler(**device)

                output = net_connect.send_command(
                    'show cdp neighbors detail', use_textfsm=True)  # Se obtiene la información
                output1 = net_connect.send_command(
                    'show ip interface brief', use_textfsm=True)  # de los output de algunos comandos
                output2 = net_connect.send_command(
                    'show running-config | include hostname')       # y se guarda en variable
                output3 = net_connect.send_command(
                    'show ip interface brief', use_textfsm=True)
                net_connect.disconnect()  # Se desconecta

                hostname = ''  # for para recuperar el hostname del dispositivo
                for f in range(len(output2)):
                    while f >= 9 and f <= len(output2):
                        hostname += output2[f]
                        break

                cont_int = (len(output3))

                # if para comprobar si es un switch o un router
                if cont_int >= 10:
                    output3 = 'Switch'
                else:
                    output3 = 'Router'
                deviceType = output3

                for x in output:
                    if x['management_ip'] not in known_ip:
                        if device_ip[0:3] in x['management_ip']:
                            known_ip.append(x['management_ip'])

                    clearly_name = ''
                    for letter in x['destination_host']:
                        if letter != '.':
                            clearly_name += letter
                        else:
                            break

                    l_neighbors.append(
                        {
                            'name': clearly_name,
                            'ip': x['management_ip'],
                            'origin': hostname,
                        }
                    )

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

            for cada in range(len(l_device)):
                for cado in range(len(l_device)):
                    # print(cada, cado)
                    if cada == cado:
                        # cambiar a break si no jala
                        continue
                    if l_device[cada]['name'] != l_device[cado]['name']:
                        if l_device[cado]['name'] not in names_list:
                            new_list.append(l_device[cado])
                            names_list.append(l_device[cado]['name'])

            # print(l_device)
            # print(new_list)
            # print(names_list)
            for leach in new_list:
                exist = Device.objects.filter(
                    device_name=leach['name']).exists()
                if not exist:
                    Device.objects.create(
                        device_username=request.POST['device_username'],
                        device_password=request.POST['device_password'],
                        device_ip=leach['ip'],
                        device_name=leach['name'],
                        device_type=leach['type']
                    )
                if exist:
                    Device.objects.filter(device_name=leach['name']).update(
                        device_username=request.POST['device_username'],
                        device_password=request.POST['device_password'],
                        device_ip=leach['ip'],
                        device_name=leach['name'],
                        device_type=leach['type']
                    )

            for laech in l_neighbors:
                Neighbor.objects.create(
                    neighbor_name=laech['name'],
                    neighbor_ip=laech['ip'],
                    origin=laech['origin']
                )

            # print(l_neighbors)
            draw_graph(l_neighbors)
            return redirect('/show_device')
        except Exception as e:
            print(e)
            return render(request, 'start.html', {
                'form': DeviceConnect,
                'error': 'La conexion no se ha encontrado'
            })


def show_device(request):
    devices = Device.objects.values_list('device_name', flat=True)
    device_list = list(devices)
    if request.method == 'POST':
        device_selected = request.POST['device']
        d_id = Device.objects.get(device_name=device_selected)
        return redirect(f'/config_device/{d_id.device_id}')
    else:
        return render(request, 'show_device.html', {
            'device_list': device_list
        })


def config_device(request, device_id: int):
    device = Device.objects.get(device_id=device_id)
    if request.method == 'POST':
        hostname = request.POST["hostname"]
        banner_motd = request.POST['banner_motd']
        ntp_server = request.POST['ntp_server']
        eneable_secret = request.POST['enable_secret']
        devices = {
            'device_type': 'cisco_ios',
            'host': device.device_ip,
            'username': device.device_username,
            'password': device.device_password
        }
        try:
            net_connect = ConnectHandler(**devices)
            net_connect.config_mode()
            if hostname:
                net_connect.send_config_set('hostname ' + hostname)
            if banner_motd:
                net_connect.send_command('banner motd #' + banner_motd + '#')
            if ntp_server:
                net_connect.send_command('ntp server ' + ntp_server)
            if eneable_secret:
                net_connect.send_command('enable secret ' + eneable_secret)
            net_connect.disconnect()
            return redirect('/show_device')
        except Exception as e:
            print(e)
            return render(request, 'config_device.html', {
                'device': device,
                'error': "Error en la conexión"
            })

    else:
        return render(request, 'config_device.html', {
            'device': device
        })


def draw_graph(l_neighbor):
    dis = []
    con = []

    for i in range(len(l_neighbor)):
        dis.append(l_neighbor[i]['name'])
        con.append(l_neighbor[i]['origin'])

    df = pd.DataFrame(list(zip(dis, con)), columns=['Dispositivo', 'Vecinos'])
    # print(df)
    plt.switch_backend('Agg')
    # df = df['Vecinos'].replace('.final.', '-', inplace=True)
    G = nx.from_pandas_edgelist(df, 'Dispositivo', 'Vecinos')
    # pos = nx.spring_layout(G)
    nx.draw_networkx(G, with_labels=True, node_size=1000, node_color="skyblue", node_shape="o", alpha=0.5, linewidths=10, font_size=15,
                     font_color="black", font_weight="bold", width=3, edge_color="grey")
    ax = plt.subplot()
    ax.set_facecolor("#f2fcff")
    ax.set_alpha(0.7)
    plt.title(label='Topología de red', fontsize=20,
              backgroundcolor="skyblue", color='white')
    plt.savefig("NetworkDiscover/static/img/Graph.png", format="PNG")
