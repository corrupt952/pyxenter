# -*- coding: utf-8 -*-

# GET IPADDRESS METHOD #
def get_vm_ipaddress(args, server):
    u"""Get IP address of VM
  
    @param args   Commnadline argument
    @param server Instance of VIServer
    """
    # Import
    import sys
    import esxi_lib
    
    index = esxi_lib.get_vm_index(server, args.vm_name)
    if index == -1:
        print >> sys.stderr, 'Not found VM.'
    else:
        # Get VM
        vm = server.get_vm_by_path(server.get_registered_vms()[index])
        
        print "Getting IP address..."
        get_ipAddress(vm, powering_on = args.powering_on, wait_time = args.wait_time)

def get_ipAddress(vm, powering_on = True, wait_time = 5):
    u"""Getting IP address of VM
    
    @param vm          Target VM
    @param powering_on After Get IP Address, VM starting flag.
    @param sleep_time  Span
    """
    # Import 
    import sys
    import time
    from pysphere import VIApiException
    
    if vm.is_powered_on() == False:
        try:
            vm.power_on()
        except VIApiException:
            print >> sys.stderr,'Cannnot powered on.'
    while vm.get_property('ip_address', from_cache = False) == None:
        print "wait...", 
        time.sleep(wait_time)
       
    print vm.get_property('ip_address', from_cache = False)
    if powering_on == False:
        try:
            vm.power_off()
        except VIApiException:
            print >> sys.stderr, 'Cannot powered off.'