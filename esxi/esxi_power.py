# -*- coding: utf-8 -*-
def power(args, server):
    u"""VM power control
    
    @param args   Commandline argument
    @param server Instance of VIServer
    """
    # Import
    import sys
    import esxi_lib

    vm = server.get_vm_by_name(args.vm_name)
    if vm <> None:
        if   args.power == 'ON':
            esxi_lib.powered_on(vm, server)
        elif args.power == 'OFF':
            esxi_lib.powered_off(vm, server)
    else:
        raise Exception('Not found VM.')