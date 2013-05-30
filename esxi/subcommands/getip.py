# -*- coding: utf-8 -*-


def set_parsers(subparsers):
    u"""Get IP Address subcommand parser.

    Add parsers in Argument subparsers.
    @param subparsers Argument Parser had subparsers
    """
    getip_parser = subparsers.add_parser('ip',
                                         help='Get VM IPaddress command.')
    getip_parser.add_argument('-H', '--host', dest='host',
                              type=str, default=None,
                              help='Host IPv4 address.')
    getip_parser.add_argument('-u', '--user', dest='user',
                              type=str, default=None,
                              help='User name.')
    getip_parser.add_argument('-p', '--password', dest='passwd',
                              type=str, default=None,
                              help='Password.')
    getip_parser.add_argument('-n', '--name', dest='vm_name',
                              type=str, default=None,
                              help='Target VM Name.', required=True)
    getip_parser.add_argument('--wait_time', dest='wait_time',
                              type=int, default=5,
                              help='Getting wait time.')
    getip_parser.set_defaults(func=get_vm_ipaddress)


def get_vm_ipaddress(args, server):
    u"""Get IP address of VM

    @param args   Commnadline argument
    @param server Instance of VIServer
    """
    # Import
    import lib

    index = lib.get_vm_index(server, args.vm_name)
    if index == -1:
        raise Exception('Not found VM.')
    else:
        # Get VM
        vm = server.get_vm_by_path(server.get_registered_vms()[index])

        print "Getting IP address..."
        get_ipAddress(vm, wait_time=args.wait_time)


def get_ipAddress(vm, wait_time=5):
    u"""Getting IP address of VM

    @param vm          Target VM
    @param powering_on After Get IP Address, VM starting flag.
    @param sleep_time  Span
    """
    # Import
    import time
    from pysphere import VIApiException

    if not vm.is_powered_on():
        raise Exception('Check power state.')
    while not vm.get_property('ip_address', from_cache=False):
        print "wait...",
        time.sleep(wait_time)

    print vm.get_property('ip_address', from_cache=False)
