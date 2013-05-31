# coding: utf-8


def set_parsers(subparsers):
    u"""Power subcommand argument.

    Add parsers in Argument subparsers.
    """

    # ON
    power_on_parser = subparsers.add_parser('on',
                                            help='Command of power on VM.')
    power_on_parser.add_argument('-U', '--url', dest='url',
                                 type=str, default=None,
                                 help='Xen Server URL.')
    power_on_parser.add_argument('-u', '--user', dest='user',
                                 type=str, default=None,
                                 help='User name.')
    power_on_parser.add_argument('-p', '--password', dest='passwd',
                                 type=str, default=None,
                                 help='User password.')
    power_on_parser.add_argument('vm_names', type=str,
                                 help='Target VM Name.', nargs='+')
    power_on_parser.set_defaults(func=power, power='ON')
    # OFF
    power_off_parser = subparsers.add_parser('off',
                                             help='Command of power off VM.')
    power_off_parser.add_argument('-U', '--url', dest='url',
                                  type=str, default=None,
                                  help='Xen Server URL.')
    power_off_parser.add_argument('-u', '--user', dest='user',
                                  type=str, default=None,
                                  help='User name.')
    power_off_parser.add_argument('-p', '--password', dest='passwd',
                                  type=str, default=None,
                                  help='User password.')
    power_off_parser.add_argument('vm_names', type=str,
                                  help='Target VM Name.', nargs='+')
    power_off_parser.set_defaults(func=power, power='OFF')
    # Reboot
    power_reboot_parser = subparsers.add_parser('reboot',
                                                help='Command of reboot VM.')
    power_reboot_parser.add_argument('-U', '--url', dest='url',
                                     type=str, default=None,
                                     help='Xen Server URL.')
    power_reboot_parser.add_argument('-u', '--user', dest='user',
                                     type=str, default=None,
                                     help='User name.')
    power_reboot_parser.add_argument('-p', '--password', dest='passwd',
                                     type=str, default=None,
                                     help='User password.')
    power_reboot_parser.add_argument('vm_names', type=str,
                                     help='Target VM Name.', nargs='+')
    power_reboot_parser.set_defaults(func=power, power='Reboot')
    # Suspend
    power_suspend_parser = subparsers.add_parser('suspend',
                                                 help='Command of suspend VM.')
    power_suspend_parser.add_argument('-U', '--url', dest='url',
                                      type=str, default=None,
                                      help='Xen Server URL.')
    power_suspend_parser.add_argument('-u', '--user', dest='user',
                                      type=str, default=None,
                                      help='User name.')
    power_suspend_parser.add_argument('-p', '--password', dest='passwd',
                                      type=str, default=None,
                                      help='User password.')
    power_suspend_parser.add_argument('vm_names', type=str,
                                      help='Target VM Name.', nargs='+')
    power_suspend_parser.set_defaults(func=power, power='Suspend')
    # Paused
    power_pause_parser = subparsers.add_parser('paused',
                                               help='Command of paused VM.')
    power_pause_parser.add_argument('-U', '--url', dest='url',
                                    type=str, default=None,
                                    help='Xen Server URL.')
    power_pause_parser.add_argument('-u', '--user', dest='user',
                                    type=str, default=None,
                                    help='User name.')
    power_pause_parser.add_argument('-p', '--password', dest='passwd',
                                    type=str, default=None,
                                    help='User password.')
    power_pause_parser.add_argument('vm_names', type=str,
                                    help='Target VM Name.', nargs='+')
    power_pause_parser.set_defaults(func=power, power='Paused')


def power(args, session):
    u"""Powered Management

    @param args    Commandline argument
    @param session Session
    """
    # Import
    import sys
    import lib

    vm_names = args.vm_names
    for vm_name in vm_names:
        # Get VM
        vm = lib.get_vm(vm_name, session)

        if vm:
            try:
                if args.power == 'ON':
                    # Powered on
                    lib.powered_on(vm, session)
                elif args.power == 'OFF':
                    # Powered off
                    lib.powered_off(vm, session)
                elif args.power == 'Reboot':
                    # Reboot
                    lib.reboot(vm, session)
                elif args.power == 'Suspend':
                    # Suspend
                    lib.suspend(vm, session)
                else:
                    # Pause
                    lib.pause(vm, session)
            except:
                print 'Power Error for VM.'
        else:
            print 'Not found VM.'
