# coding: utf-8

def args():
    u"""引数のパーサを構築
    
    パーサを構築し、構築したパーサのargumentを返す
    @return 構築したパーサのargument
    """
    # Import
    import argparse
    import xen_list
    import xen_destroy
    import xen_install
    import xen_power
    import xen_getip
   
    # Parent parser
    parser = argparse.ArgumentParser(description='Xen tool')
   
    # Sub parsers
    subparsers = parser.add_subparsers(help='commands.')
   
    # List parser
    list_parser = subparsers.add_parser('list', help='Command of vm list.')
    list_parser.add_argument('-U', '--url',       dest = 'url',
                                type = str,       default = None,
                                help = 'Xen Server URL.')
    list_parser.add_argument('-u', '--user',      dest = 'user',
                                type = str,       default = None,
                                help = 'User name.')
    list_parser.add_argument('-p', '--password',  dest = 'passwd',
                                type = str,       default = None,
                                help = 'User password.')
    list_parser.add_argument('-t', '--template',  dest='template',
                                action = 'store_true',      default = False,
                                help = 'Template list.')
    list_parser.set_defaults(func=xen_list.show_vm_list)
    
    # Destroy parser
    destroy_parser = subparsers.add_parser('destroy', help='Command of Destroy VM.')
    destroy_parser.add_argument('-U', '--url',      dest = 'url',
                                  type = str,       default = None,
                                  help = 'Xen Server URL.')
    destroy_parser.add_argument('-u', '--user',     dest = 'user',
                                  type = str,       default = None,
                                  help = 'User name.')
    destroy_parser.add_argument('-p', '--password', dest = 'passwd',
                                  type = str,       default = None,
                                  help = 'User password.')
    destroy_parser.add_argument('-n', '--name',     dest = 'vm_name',
                                  type = str,       default = None,
                                  help = 'Target VM Name.', required=True)
    destroy_parser.set_defaults(func=xen_destroy.destroy)
    
    # Install parser(use template)
    install_parser = subparsers.add_parser('install', help='Command of install VM.')
    install_parser.add_argument('-U','--url',        dest    = 'url',
                                  type = str,        default = None,
                                  help = 'Xen server URL.')
    install_parser.add_argument('-u','--user',       dest    = 'user',
                                  type = str,        default = None,
                                  help = 'User name.')
    install_parser.add_argument('-p','--password',   dest    = 'passwd',
                                  type = str,        default = None,
                                  help = 'User password.')
    install_parser.add_argument('-n','--name',       dest    = 'vm_name',
                                  type = str,        default = None,
                                  help = 'New VM name.',      required = True)
    install_parser.add_argument('-t','--template',   dest    = 'temp_name',
                                  type = str,        default = None,
                                  help = 'VM template name.', required = True)
    install_parser.set_defaults(func=xen_install.vm_install)
    
    # Power parser
    # ON
    power_on_parser = subparsers.add_parser('on', help='Command of power off for VM.')
    power_on_parser.add_argument('-U', '--url',      dest = 'url',
                                  type = str,        default = None,
                                  help = 'Xen Server URL.')
    power_on_parser.add_argument('-u', '--user',     dest = 'user',
                                  type = str,        default = None,
                                  help = 'User name.')
    power_on_parser.add_argument('-p', '--password', dest = 'passwd',
                                  type = str,        default = None,
                                  help = 'User password.')
    power_on_parser.add_argument('-n', '--name',     dest = 'vm_name',
                                  type = str,        default = None,
                                  help = 'Target VM Name.', required=True)
    power_on_parser.set_defaults(func=xen_power.power, power = 'ON')
    # OFF
    power_off_parser = subparsers.add_parser('off', help='Command of power off for VM.')
    power_off_parser.add_argument('-U', '--url',      dest = 'url',
                                  type = str,         default = None,
                                  help = 'Xen Server URL.')
    power_off_parser.add_argument('-u', '--user',     dest = 'user',
                                  type = str,         default = None,
                                  help = 'User name.')
    power_off_parser.add_argument('-p', '--password', dest = 'passwd',
                                  type = str,         default = None,
                                  help = 'User password.')
    power_off_parser.add_argument('-n', '--name',     dest = 'vm_name',
                                  type = str,         default = None,
                                  help = 'Target VM Name.', required=True)
    power_off_parser.set_defaults(func=xen_power.power, power = 'OFF')
    # Reboot
    power_reboot_parser = subparsers.add_parser('reboot', help='Command of reboot for VM.')
    power_reboot_parser.add_argument('-U', '--url',      dest = 'url',
                                  type = str,         default = None,
                                  help = 'Xen Server URL.')
    power_reboot_parser.add_argument('-u', '--user',     dest = 'user',
                                  type = str,         default = None,
                                  help = 'User name.')
    power_reboot_parser.add_argument('-p', '--password', dest = 'passwd',
                                  type = str,         default = None,
                                  help = 'User password.')
    power_reboot_parser.add_argument('-n', '--name',     dest = 'vm_name',
                                  type = str,         default = None,
                                  help = 'Target VM Name.', required=True)
    power_reboot_parser.set_defaults(func=xen_power.power, power = 'Reboot')
    # Suspend
    power_suspend_parser = subparsers.add_parser('suspend', help='Command of suspend for VM.')
    power_suspend_parser.add_argument('-U', '--url',      dest = 'url',
                                  type = str,         default = None,
                                  help = 'Xen Server URL.')
    power_suspend_parser.add_argument('-u', '--user',     dest = 'user',
                                  type = str,         default = None,
                                  help = 'User name.')
    power_suspend_parser.add_argument('-p', '--password', dest = 'passwd',
                                  type = str,         default = None,
                                  help = 'User password.')
    power_suspend_parser.add_argument('-n', '--name',     dest = 'vm_name',
                                  type = str,         default = None,
                                  help = 'Target VM Name.', required=True)
    power_suspend_parser.set_defaults(func=xen_power.power, power = 'Suspend')
    # Paused
    power_pause_parser = subparsers.add_parser('paused', help = 'Command of paused for VM.')
    power_pause_parser.add_argument('-U', '--url',      dest    = 'url',
                                  type = str,           default = None,
                                  help = 'Xen Server URL.')
    power_pause_parser.add_argument('-u', '--user',     dest    = 'user',
                                  type = str,           default = None,
                                  help = 'User name.')
    power_pause_parser.add_argument('-p', '--password', dest    = 'passwd',
                                  type = str,           default = None,
                                  help = 'User password.')
    power_pause_parser.add_argument('-n', '--name',     dest    = 'vm_name',
                                  type = str,           default = None,
                                  help = 'Target VM Name.', required=True)
    power_pause_parser.set_defaults(func=xen_power.power, power = 'Paused')
    
    # Get IP Parser
    getip_parser = subparsers.add_parser('ip', help = 'Command of show VM\'s IP address.')
    getip_parser.add_argument('-U', '--url',        dest    = 'url',
                                    type = str,     default = None,
                                    help = 'Xen Server URL.')
    getip_parser.add_argument('-u', '--user',       dest    = 'user',
                                    type = str,     default = None,
                                    help = 'User name.')
    getip_parser.add_argument('-p', '--password',   dest    = 'passwd',
                                    type = str,     default = None,
                                    help = 'User password.')
    getip_parser.add_argument('-n', '--name',       dest    = 'vm_name',
                                    type = str,     default = None,
                                    help = 'Target VM Name.', required=True)
    getip_parser.add_argument('--wait_time',        dest    ='wait_time',
                                    type = int,     default = 3,
                                    help = 'Getting wait time.')
    getip_parser.set_defaults(func=xen_getip.vm_ipaddress)
    
    # Return
    return parser.parse_args()