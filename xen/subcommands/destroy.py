# coding: utf-8


def set_parsers(subparsers):
    u""" Destroy subcommand parser.

    Add parsers int Argument subparsers.
    """
    destroy_parser = subparsers.add_parser('destroy',
                                           help='Command of Destroy VM.')
    destroy_parser.add_argument('-U', '--url', dest='url',
                                type=str, default=None,
                                help='Xen Server URL.')
    destroy_parser.add_argument('-u', '--user', dest='user',
                                type=str, default=None,
                                help='User name.')
    destroy_parser.add_argument('-p', '--password', dest='passwd',
                                type=str, default=None,
                                help='User password.')
    destroy_parser.add_argument('-n', '--name', dest='vm_names',
                                type=str, default=None,
                                help='Target VM Name.', required=True,
                                nargs='+')
    destroy_parser.set_defaults(func=destroy)


def destroy(args, session):
    u"""Destroying VM

    @param args    Commandline argument
    @param session Session
    """
    # Import
    import lib

    vm_names = args.vm_names
    for vm_name in vm_names:
        # Set VM name
        vm = lib.get_vm(vm_name, session)
        if vm:
            try:
                print 'Destroying...'
                vdis = lib.get_storage_vdis(vm, session)
                if vdis:
                    for vdi in vdis:
                        session.xenapi.VDI.destroy(vdi)

                session.xenapi.VM.destroy(vm)
                print '%s Done.' % vm_name
            except Exception, e:
                print 'Please shutdown for VM.'
        else:
            print 'Not found VM.'
