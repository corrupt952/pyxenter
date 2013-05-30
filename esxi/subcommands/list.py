# -*- coding: utf-8 -*-


def set_parsers(subparsers):
    u"""VM List subcommand parser.

    Add parsers in Argument subparsers.
    @param subparsers Argument Parser had subparsers
    """
    list_parser = subparsers.add_parser('list', help='VM list command.')
    list_parser.add_argument('-H', '--host', dest='host',
                             type=str, default=None,
                             help='Host IPv4 address.')
    list_parser.add_argument('-u', '--user', dest='user',
                             type=str, default=None,
                             help='User name.')
    list_parser.add_argument('-p', '--password', dest='passwd',
                             type=str, default=None,
                             help='Password.')
    list_parser.set_defaults(func=show_vm_list)


def show_vm_list(args, server):
    u"""Show List of server has any VM.

    @param args   Commandline argument
    @param server Instance of VIServer
    """
    vm_paths = server.get_registered_vms()
    print '|          Name          | Power state | IP address |'
    for vm_path in vm_paths:
        vm = server.get_vm_by_path(vm_path)
        print
        # VM name
        print "| %20s" % vm.get_property('name'),
        # Power state
        power_state = 'Halted'
        if vm.is_powered_on():
            power_state = 'Running'
        print "| %11s " % power_state,
        print "| %10s |" % vm.get_property('ip_address', from_cache=False)
    print
