# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404

from pysphere import VIServer
from esxi.subcommands import lib

def index(request):
    host = '192.168.7.186'
    user = 'root'
    passwd = 'tim9009'
    server = VIServer()
    server.connect(host, user, passwd)
    vm_paths = server.get_registered_vms()
    th_list = ['Name', 'Power state', 'IP address']
    vm_list = []
    for vm_path in vm_paths:
        vm_data = []
        vm = server.get_vm_by_path(vm_path)
        vm_data.append(vm.get_property('name'))
        vm_data.append('Halted')
        if vm.is_powered_on():
            vm_data[vm_data.index('Halted')] = 'Running'
        vm_data.append(vm.get_property('ip_address', from_cache=False))
        vm_list.append(vm_data)
    return render_to_response('esxi/index.html', {'vm_list': vm_list, 'title':host, 'th_list':th_list})

