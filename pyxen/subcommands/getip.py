# -*- coding: utf-8 -*-


def set_parsers(subparsers):
    u""" Getting IP address subcommand parser.

    Add parsers int Argument subparsers.
    """
    getip_parser = subparsers.add_parser('ip',
                                         help="Command of VM's IP address.")
    getip_parser.add_argument('-U', '--url', dest='url',
                              type=str, default=None,
                              help='Xen Server URL.')
    getip_parser.add_argument('-u', '--user', dest='user',
                              type=str, default=None,
                              help='User name.')
    getip_parser.add_argument('-p', '--password', dest='passwd',
                              type=str, default=None,
                              help='User password.')
    getip_parser.add_argument('-n', '--name', dest='vm_name',
                              type=str, default=None,
                              help='Target VM Name.', required=True)
    getip_parser.add_argument('--wait_time', dest='wait_time',
                              type=int, default=3,
                              help='Getting wait time.')
    getip_parser.set_defaults(func=vm_ipaddress)


def vm_ipaddress(args, session):
    u"""Show ipaddress.

    @param args    Commandline argument
    @param session Session
    """
    # Import
    import lib
    import time

    vm = lib.get_vm(args.vm_name, session)
    vm_record = session.xenapi.VM.get_record(vm)

    if vm_record['is_a_template']:
        # Check template
        raise Exception('%s is template.' % args.vm_name)
    if vm_record['power_state'] != 'Running':
        # Check power state.
        raise Exception('Power state is %s.' % vm_record['power_state'])
    if vm_record['guest_metrics'].split(':')[1] == 'NULL':
        # Check xen tools
        raise Exception('Xen tools is not installed.')

    # Getting IP address.
    while lib.get_ip_address(vm, session):
        print 'wait...',
        time.sleep(args.wait_time)
    print ''
    print 'IP address : %s' % lib.get_ip_address(vm, session)
    print 'Done.'
