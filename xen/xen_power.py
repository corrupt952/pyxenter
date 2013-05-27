# coding: utf-8

def power(args, session):
    u"""Powered Management
   
    @param args    Commandline argument
    @param session Session
    """
    # Import
    import sys
    import xen_lib
   
    # Get VM
    vm = xen_lib.get_vm(args.vm_name, session)
   
    if not vm == None:
        #try:
            if args.power == 'ON':
                # Powered on
                xen_lib.powered_on(vm, session)
            elif args.power == 'OFF':
                # Powered off
                xen_lib.powered_off(vm, session)
            elif args.power == 'Reboot':
                # Reboot
                xen_lib.reboot(vm, session)
            elif args.power == 'Suspend':
                # Suspend
                xen_lib.suspend(vm, session)
            else:
                # Pause
                xen_lib.pause(vm, session)
       # except:
        #    raise Exception('Power Error for VM.')
    else:
        raise Exception('Not found VM.')