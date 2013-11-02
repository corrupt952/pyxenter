# -*- coding: utf-8 -*-


def set_parsers(subparsers):
    u"""Powered subcommand parser.

    Add parsers in Argument subparsers.
    @param subparsers Argument Parser had subparsers
    """
    # ON
    power_on_parser = subparsers.add_parser('on', help='Power on VM.')
    power_on_parser.add_argument('-H', '--host', dest='host',
                                 type=str, default=None,
                                 help='Host IPv4 address.')
    power_on_parser.add_argument('-u', '--user', dest='user',
                                 type=str, default=None,
                                 help='User name.')
    power_on_parser.add_argument('-p', '--password', dest='passwd',
                                 type=str, default=None,
                                 help='Password.')
    power_on_parser.add_argument('vm_names', type=str,
                                 help='Target VM Names.', nargs='+')
    power_on_parser.set_defaults(func=power, power='ON')
    # OFF
    power_off_parser = subparsers.add_parser('off', help='Power off VM.')
    power_off_parser.add_argument('-H', '--host', dest='host',
                                  type=str, default=None,
                                  help='Host IPv4 address.')
    power_off_parser.add_argument('-u', '--user', dest='user',
                                  type=str, default=None,
                                  help='User name.')
    power_off_parser.add_argument('-p', '--password', dest='passwd',
                                  type=str, default=None,
                                  help='Password.')
    power_off_parser.add_argument('vm_names', type=str,
                                  help='Target VM Names.', nargs='+')
    power_off_parser.set_defaults(func=power, power='OFF')
    # Suspend
    power_suspend_parser = subparsers.add_parser('suspend',
                                                 help='Command of suspend VM.')
    power_suspend_parser.add_argument('-H', '--host', dest='host',
                                 type=str, default=None,
                                 help='Host IPv4 address.')
    power_suspend_parser.add_argument('-u', '--user', dest='user',
                                      type=str, default=None,
                                      help='User name.')
    power_suspend_parser.add_argument('-p', '--password', dest='passwd',
                                      type=str, default=None,
                                      help='User password.')
    power_suspend_parser.add_argument('vm_names', type=str,
                                      help='Target VM Name.', nargs='+')
    power_suspend_parser.set_defaults(func=power, power='Suspend')

def power(args, server):
    u"""VM power control

    @param args   Commandline argument
    @param server Instance of VIServer
    """
    # Import
    import lib

    vm_names = args.vm_names
    for vm_name in vm_names:
        try:
            vm = server.get_vm_by_name(vm_name)
            if args.power == 'ON':
                lib.powered_on(vm, server)
            elif args.power == 'OFF':
                lib.powered_off(vm, server)
            elif args.power == 'Suspend':
                lib.suspend(vm, server)

            print '%s Done.' % vm_name
        except Exception, (strerror):
            print strerror
