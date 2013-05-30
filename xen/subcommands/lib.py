# coding: utf-8


def get_vm(vm_name, session):
    u"""Getting VM

    If exists vm, return VM.
    Otherwise return None.

    @param vm_name VM's name
    @param session　Session

    @return VM or None
    """
    vm = None
    vms = session.xenapi.VM.get_by_name_label(vm_name)
    if len(vms) == 1:
        return vms[0]
    return vm


def get_ip_address(vm, session):
    u""" Getting VM IPaddress

    If got ip address, return ip address of str type.
    Otherwise return None.

    @param vm      VM
    @param session Session

    @return Ip address or None
    """
    vgm = session.xenapi.VM.get_guest_metrics(vm)
    try:
        networks = session.xenapi.VM_guest_metrics.get_networks(vgm)
        if '0/ip' in networks.keys():
            return networks['0/ip']
        return None
    except:
        return None


def get_storage_vdis(vm, session):
    u"""Get VDIs

    Return list has VM's any VDIs.

    @param vm      VM
    @param session Session

    @return VDI List
    """
    vdis = []

    vbds = session.xenapi.VM.get_VBDs(vm)
    for vbd in vbds:
        vdi = session.xenapi.VBD.get_VDI(vbd)
        vdi_records = session.xenapi.VDI.get_all_records()
        xenstore_data = vdi_records[vdi]['xenstore_data']
        if vdi.split(':')[1] != 'NULL' \
                and xenstore_data != {}:
            vdis.append(vdi)
    return vdis


def powered_on(vm, session):
    u"""VM start

    Power state being 'Running'

    @param vm      VM
    @param session Session
    """
    # Get power state.
    power_state = session.xenapi.VM.get_power_state(vm)

    if power_state == 'Running':
        print 'Already powered on.'
    elif power_state == 'Paused':
        print 'Continuing...'
        session.xenapi.VM.unpause(vm)
        print 'Done.'
    elif power_state == 'Suspended':
        print 'Resuming...'
        session.xenapi.VM.resume(vm, False, True)
        print 'Done.'
    else:
        print 'Powered on...'
        session.xenapi.VM.start(vm, False, True)
        print 'Done.'


def powered_off(vm, session):
    u"""VM shutdown.

    Power state being 'Halted'
    @param vm      VM
    @param session Session
    """
    #　Check Xen tools
    vm_shutdown = session.xenapi.VM.hard_shutdown
    guest_metrics = session.xenapi.VM.get_record(vm)['guest_metrics']
    if guest_metrics.split(':')[1] != 'NULL':
        vm_shutdown = session.xenapi.VM.clean_shutdown

    # Get power state.
    power_state = session.xenapi.VM.get_power_state(vm)

    if power_state == 'Running':
        print 'Powered off...'
        vm_shutdown(vm)
        print 'Done.'
    elif power_state == 'Paused':
        powered_on(vm, session)
        print 'Powered off...'
        vm_shutdown(vm)
        print 'Done.'
    elif power_state == 'Suspended':
        powered_on(vm, session)
        print 'Powered off...'
        vm_shutdown(vm)
        print 'Done.'
    else:
        print 'Already powered off.'


def reboot(vm, session):
    u"""VM reboot

    After power state being 'Halted',
    Power state being 'Running'.

    @param vm      VM
    @param session Session
    """
    # Check Xen tools
    vm_reboot = session.xenapi.VM.hard_reboot
    guest_metrics = session.xenapi.VM.get_record(vm)['guest_metrics']
    if guest_metrics.split(':')[1] != 'NULL':
        vm_reboot = session.xenapi.VM.clean_reboot

    # Get power state.
    power_state = session.xenapi.VM.get_power_state(vm)

    if power_state == 'Running':
        print 'Rebooting...'
        vm_reboot(vm)
        print 'Done.'
    elif power_state == 'Paused':
        powered_on(vm, session)
        print 'Rebooting...'
        vm_reboot(vm)
        print 'Done.'
    elif power_state == 'Suspended':
        powered_on(vm, session)
        print 'Rebooting...'
        vm_reboot(vm)
        print 'Done.'
    else:
        powered_on(vm, session)


def suspend(vm, session):
    u"""VM suspend

    Power state being 'Suspend'

    @param vm      VM
    @param session Session
    """
    # Check Xen tools
    guest_metrics = session.xenapi.VM.get_record(vm)['guest_metrics']
    if guest_metrics.split(':')[1] != 'NULL':
        raise Exception('Xen tools is not installed.')

    # Get power state
    power_state = session.xenapi.VM.get_power_state(vm)

    if power_state == 'Running':
        print 'Suspending...'
        session.xenapi.VM.suspend(vm)
        print 'Done.'
    else:
        print 'Cannot suspend.'


def pause(vm, session):
    u"""VM pause

    Power state being 'Paused'

    @param vm      VM
    @param session Session
    """
    # Get power state
    power_state = session.xenapi.VM.get_power_state(vm)

    if power_state == 'Running':
        print 'Pausing...'
        session.xenapi.VM.pause(vm)
        print 'Done.'
    else:
        print 'Cannot paused.'


def install(vm_name, template_name, session):
    u"""Install New VM, using template

    @param vm_name       VM Name
    @param template_name Template Name
    @param session       Session

    @return New VM
    """
    pifs = session.xenapi.PIF.get_all_records()
    lowest = reduce(lambda a, b: min(pifs[a]['device'],
                                     pifs[b]['device']),
                    pifs)

    # Network
    network = session.xenapi.PIF.get_network(lowest)

    # List all the VM
    vms = session.xenapi.VM.get_all_records()

    templates = []
    for vm in vms:
        record = vms[vm]
        # Check template
        if record["is_a_template"]:
            # Check name label
            if record["name_label"] == template_name:
                templates.append(vm)
    if templates == []:
        raise Excenption('Could not find template.')

    template = templates[0]
    session.xenapi.VM.get_name_label(template)
    print "Installing..."
    vm = session.xenapi.VM.clone(template, vm_name)
    vbds = session.xenapi.VM.get_VBDs(vm)
    for vbd in vbds:
        vdis = get_storage_vdis(vm, session)
        for vdi in vdis:
            vm_name = session.xenapi.VM.get_name_label(vm)
            session.xenapi.VDI.set_name_label(vdi, vm_name)
    # Template flag
    session.xenapi.VM.set_is_a_template(vm, False)
    session.xenapi.VM.set_PV_args(vm, "noninteractive")

    return vm
