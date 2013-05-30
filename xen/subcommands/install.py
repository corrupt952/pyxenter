# -*- coding: utf8 -*-


def set_parsers(subparsers):
    u"""Install subcommand argument.

    Add parsers int Argument subparsers.
    """
    install_parser = subparsers.add_parser('install',
                                           help='Command of install VM.')
    install_parser.add_argument('-U', '--url', dest='url',
                                type=str, default=None,
                                help='Xen server URL.')
    install_parser.add_argument('-u', '--user', dest='user',
                                type=str, default=None,
                                help='User name.')
    install_parser.add_argument('-p', '--password', dest='passwd',
                                type=str, default=None,
                                help='User password.')
    install_parser.add_argument('-n', '--name', dest='vm_names',
                                type=str, default=None,
                                help='New VM name.', required=True,
                                nargs='+')
    install_parser.add_argument('-t', '--template', dest='temp_name',
                                type=str, default=None,
                                help='VM template name.', required=True)
    install_parser.set_defaults(func=vm_install)


def vm_install(args, session):
    u"""Install VM(use template)

    @param args    CommandLien argument
    @param session Session
    """
    # Import
    import lib

    vm_names = args.vm_names
    for vm_name in vm_names:
        if lib.get_vm(vm_name, session):
            print 'Already exist VM.'
        else:
            # Instal
            vm = lib.install(vm_name,
                             args.temp_name,
                             session)

            print '%s Done.' % vm_name

            # VM start
            print 'Starting...'
            try:
                session.xenapi.VM.start(vm, False, True)
            except:
                print 'Cannot started VM.'
