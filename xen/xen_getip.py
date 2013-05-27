# -*- coding: utf-8 -*-

def vm_ipaddress(args, session):
    u"""Show ipaddress.
    
    @param args    Commandline argument
    @param session Session
    """
    # Import
    import xen_lib
    import time
    
    vm = xen_lib.get_vm(args.vm_name, session)
    vm_record = session.xenapi.VM.get_record(vm)
    
    if vm_record['is_a_template']:
        # Check template
        raise Exception('%s is template.' % args.vm_name)
    if vm_record['power_state'] <> 'Running':
        # Check power state.
        raise Exception('Power state is %s.' % vm_record['power_state'])
    if vm_record['guest_metrics'].split(':')[1] == 'NULL':
        # Check xen tools
        raise Exception('Xen tools is not installed.')
    
    # Getting IP address.
    while xen_lib.get_ip_address(vm, session) == None:
        print 'wait...',
        time.sleep(args.wait_time)
    print ''
    print 'IP address : %s' % xen_lib.get_ip_address(vm, session)
    print 'Done.'