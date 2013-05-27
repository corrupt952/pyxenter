# -*- coding: utf-8 -*-

# DESTROY VM METHOD #
def destroy_vm(args, server):
    u"""Destroy VM
    
    @param args   Commandline argument
    @param server Instance of VIServer
    """
    # Import
    import sys
    from pysphere import VIApiException, VIException
    import esxi_lib
    
    try:
       esxi_lib.delete_vm_by_name(args.vm_name, server)
    except VIApiException:
       print >> sys.stderr, 'Cannot deleted.'
    except VIException:
       print >> sys.stderr, 'Not found VM.'