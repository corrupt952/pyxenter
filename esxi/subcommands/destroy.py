# -*- coding: utf-8 -*-


def set_parsers(subparsers):
    u"""Destroy subcommand parser.

    Add parsers in Argument subparsers.
    @param subparsers Argument Parser had subparsers
    """
    destroy_parser = subparsers.add_parser('destroy',
                                           help='Destroy VM command.')
    destroy_parser.add_argument('-H', '--host', dest='host',
                                type=str, default=None,
                                help='Host IPv4 address.')
    destroy_parser.add_argument('-u', '--user', dest='user',
                                type=str, default=None,
                                help='User name.')
    destroy_parser.add_argument('-p', '--password', dest='passwd',
                                type=str, default=None,
                                help='Password.')
    destroy_parser.add_argument('-n', '--name', dest='vm_name',
                                type=str, default=None,
                                help='Target VM Name.', required=True)
    destroy_parser.set_defaults(func=destroy_vm)


def destroy_vm(args, server):
    u"""Destroy VM

    @param args   Commandline argument
    @param server Instance of VIServer
    """
    # Import
    from pysphere import VIApiException, VIException
    import lib

    try:
        lib.delete_vm_by_name(args.vm_name, server)
    except VIApiException:
        raise Exception('Cannot deleted.')
    except VIException:
        raise Exception('Not found VM.')
