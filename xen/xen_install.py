# -*- coding: utf8 -*-

def vm_install(args, session):
    u"""Install VM(use template)
   
    @param args    CommandLien argument
    @param session Session
    """
    # Import
    import xen_lib
    
    if xen_lib.get_vm(args.vm_name, session) <> None:
        raise Exception('Already exist VM.')
    
    # Instal
    vm = xen_lib.install(args.vm_name, args.temp_name, session)
    
    # VM start
    print 'Starting...'
    session.xenapi.VM.start(vm, False, True)
    
    print 'Done.'