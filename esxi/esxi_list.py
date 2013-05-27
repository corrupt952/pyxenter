# -*- coding: utf-8 -*-

# SHOW VM LIST METHOD #
def show_vm_list(args, server):
    u"""Show List of server has any VM.
    
    @param args   Commandline argument
    @param server Instance of VIServer
    """
    vm_paths = server.get_registered_vms()
    print
    for vm_path in vm_paths:
        vm = server.get_vm_by_path(vm_path)
        print
        # VM name
        print "VM: %s" % vm.get_property('name')
        # Power state
        power_state = 'Halted'
        if vm.is_powered_on() == True:
            power_state = 'Running'
        print "Power State: %s" % power_state
    print