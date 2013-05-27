# -*- coding: utf-8 -*-

def args():
    u"""Set argument.
    
    @return argument
    """
    # Import 
    import argparse
    import esxi_list
    import esxi_destroy
    import esxi_deploy
    import esxi_getip
    import esxi_power
    
    # Parent parser
    parser = argparse.ArgumentParser(description='ESXi Tools')
    
    # Sub parser
    subparsers = parser.add_subparsers(help='commands')
    
    # List parser
    list_parser = subparsers.add_parser('list', help='VM list command.')
    list_parser.add_argument('-H', '--host',     dest = 'host',   type = str, default = None)
    list_parser.add_argument('-u', '--user',     dest = 'user',   type = str, default = None)
    list_parser.add_argument('-p', '--password', dest = 'passwd', type = str, default = None)
    list_parser.set_defaults(func=esxi_list.show_vm_list)
    
    # Destroy parser
    destroy_parser = subparsers.add_parser('destroy', help='Destroy VM command.')
    destroy_parser.add_argument('-H', '--host',     dest = 'host',    type = str, default = None)
    destroy_parser.add_argument('-u', '--user',     dest = 'user',    type = str, default = None)
    destroy_parser.add_argument('-p', '--password', dest = 'passwd',  type = str, default = None)
    destroy_parser.add_argument('-n', '--name',     dest = 'vm_name', type = str, default = None, help='Target VM Name.', required=True)
    destroy_parser.set_defaults(func=esxi_destroy.destroy_vm)
    
    # Deploy parser
    deploy_parser = subparsers.add_parser('import', help='Import VM image command.')
    deploy_parser.add_argument('-H', '--host',     dest = 'host',   type = str, default = None)
    deploy_parser.add_argument('-u', '--user',     dest = 'user',   type = str, default = None)
    deploy_parser.add_argument('-p', '--password', dest = 'passwd', type = str, default = None)
    deploy_group = deploy_parser.add_mutually_exclusive_group()
    deploy_group.add_argument( '--file',         dest = 'file_path',     type = str, default = None)
    deploy_group.add_argument( '--url',          dest = 'file_url',      type = str, default = None)
    deploy_parser.add_argument('-n', '--name',   dest = 'vm_name',       type = str, default = None)
    deploy_parser.add_argument('--datacenter',   dest = 'datacenter',    type = str, default = None)
    deploy_parser.add_argument('--datastore',    dest = 'datastore',     type = str, default = None)
    deploy_parser.add_argument('--resourcepool', dest = 'resource_pool', type = str, default = None)
    deploy_parser.add_argument('--network',      dest = 'network',       type = str, default = None)
    deploy_parser.set_defaults(func=esxi_deploy.deploy_vm)
    
    # IP parser
    getip_parser = subparsers.add_parser('ip',help='Get VM IPaddress command.')
    getip_parser.add_argument('-H', '--host',     dest = 'host',        type = str,           default = None)
    getip_parser.add_argument('-u', '--user',     dest = 'user',        type = str,           default = None)
    getip_parser.add_argument('-p', '--password', dest = 'passwd',      type = str ,          default = None)
    getip_parser.add_argument('-n', '--name',     dest = 'vm_name',     type = str,           default = None, help='Target VM Name.', required=True)
    getip_parser.add_argument('--powering_off',   dest = 'powering_on', action='store_false', default = True)
    getip_parser.add_argument('--wait_time',      dest = 'wait_time',   type = int ,          default = 5)
    getip_parser.set_defaults(func=esxi_getip.get_vm_ipaddress)
    
    # Power parser
    # ON
    power_on_parser  = subparsers.add_parser('on', description='')
    power_on_parser.add_argument('-H', '--host',     dest = 'host',
                                 type = str,         default = None)
    power_on_parser.add_argument('-u', '--user',     dest = 'user',
                                 type = str,         default = None)
    power_on_parser.add_argument('-p', '--password', dest = 'passwd',
                                 type = str ,        default = None)
    power_on_parser.add_argument('-n', '--name',     dest = 'vm_name',
                                 type = str,         default = None,
                                 help='Target VM Name.', required=True)
    power_on_parser.set_defaults(func=esxi_power.power, power='ON')
    # OFF
    power_off_parser = subparsers.add_parser('off')
    power_off_parser.add_argument('-H', '--host',     dest = 'host',
                                 type = str,         default = None)
    power_off_parser.add_argument('-u', '--user',     dest = 'user',
                                 type = str,         default = None)
    power_off_parser.add_argument('-p', '--password', dest = 'passwd',
                                 type = str ,        default = None)
    power_off_parser.add_argument('-n', '--name',     dest = 'vm_name',
                                 type = str,         default = None,
                                 help='Target VM Name.', required=True)
    power_off_parser.set_defaults(func=esxi_power.power, power='OFF')
    
    return parser.parse_args()