# coding: utf-8


def set_parsers(subparsers):
    u"""List subcommand argument.

    Add parsers int Argument subparsers.
    """
    list_parser = subparsers.add_parser('list', help='Command of vm list.')
    list_parser.add_argument('-U', '--url', dest='url',
                             type=str, default=None,
                             help='Xen Server URL.')
    list_parser.add_argument('-u', '--user', dest='user',
                             type=str, default=None,
                             help='User name.')
    list_parser.add_argument('-p', '--password', dest='passwd',
                             type=str, default=None,
                             help='User password.')
    list_parser.add_argument('-t', '--template', dest='template',
                             action='store_true', default=False,
                             help='Template list.')
    list_parser.set_defaults(func=show_vm_list)


def show_vm_list(args, session):
    u"""Show vm list

    @param args    Commandline argumetn
    @param session Session
    """
    # Import
    import lib

    # Get VMs
    vms = session.xenapi.VM.get_all()

    print
    print '|      Name     |  Power   |    Xen Tools   |    IP Address    |'
    print '----------------------------------------------------------------'
    for vm in vms:
        record = session.xenapi.VM.get_record(vm)
        if not record["is_control_domain"] \
                and not 'Transfer' in record["name_label"] \
                and record["is_a_template"] == args.template:
            # Print VMs
            print "| %12s " % record['name_label'] ,
            print "| %7s " % record['power_state'] ,
            tool_state = record['guest_metrics'].split(':')[1]
            print "| %13s " % ('Installed' if tool_state != 'NULL' else 'Not installed'),
            print "| %16s |" % lib.get_ip_address(vm, session)
