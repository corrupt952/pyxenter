# -*- coding: utf-8 -*-


def set_parsers(subparsers):
    u"""Deploy subcommand parser.

    Add parsers in Argument subparsers.
    @param subparsers Argument Parser had subparsers
    """
    deploy_parser = subparsers.add_parser('import',
                                          help='Import VM image command.')
    deploy_parser.add_argument('-H', '--host', dest='host',
                               type=str, default=None,
                               help='Host IPv4 address.')
    deploy_parser.add_argument('-u', '--user', dest='user',
                               type=str, default=None,
                               help='User name.')
    deploy_parser.add_argument('-p', '--password', dest='passwd',
                               type=str, default=None,
                               help='Password.')
    # Deploy group
    deploy_group = deploy_parser.add_mutually_exclusive_group(required=True)
    deploy_group.add_argument('--file', dest='filepath',
                              type=str, default=None,
                              help='OVF or OVA File Path.')
    deploy_group.add_argument('--url', dest='file_url',
                              type=str, default=None,
                              help='OVA File URL.')

    deploy_parser.add_argument('-n', '--name', dest='vm_names',
                               type=str, default=None,
                               help='New VM name.', required=True,
                               nargs='+')
    deploy_parser.add_argument('--datacenter', dest='datacenter',
                               type=str, default=None,
                               help='Datacenter name.')
    deploy_parser.add_argument('--datastore', dest='datastore',
                               type=str, default=None,
                               help='Datastore name.')
    deploy_parser.add_argument('--resourcepool', dest='resource_pool',
                               type=str, default=None,
                               help='Resource Pool path.')
    deploy_parser.add_argument('--network', dest='network',
                               type=str, default=None,
                               help='Network Name.')
    deploy_parser.set_defaults(func=deploy_vm)


# DEPLOY METHOD #
def deploy_vm(args, server):
    u"""Deploy VM(import)

    @param args   Commandline argument
    @param server Instance of VIServer
    """
    # Import
    import os
    import shutil
    from pysphere import VIMor
    import lib

    download_temp = './temp/'
    extract_temp = None

    try:
        # Download
        if args.file_url:
            if args.file_url.find('.ova') > 0:
                args.filepath = lib.download_file(args.file_url, download_temp)
            else:
                raise Excepiton('File format not supported.')

        filepath = args.filepath
        if os.path.exists(filepath):
            raise Exception("File not found.")

        if filepath.find('.ova') > 0:
            #  If  file format is ova
            file_name = filepath.split('/')[-1]
            extract_temp = r"./%s/" % file_name.replace('.ova', '')
            filepath = lib.ova_extract(filepath, extract_temp)
        elif filepath.find('.ovf') < 0:
            # If file format isn't ova and ovf
            raise Exception("File format not supported.")

        # ovf_filepath path
        ovf_filepath = filepath
        lib.check_ovf(ovf_filepath)

        # Remove mf File
        MF_FILE = ovf_filepath.replace('.ovf', '.mf')
        if os.path.exists(MF_FILE):
            os.remove(MF_FILE)

        # Host
        if not args.datacenter:
            host_name = server.get_hosts().values()[0]
        else:
            host_name = VIMor(args.datacenter,
                              MORTypes.Datacenter)

        # Datastore
        if not args.datastore:
            datastore_name = server.get_datastores().values()[0]
        else:
            datastore_name = VIMor(args.datastore,
                                   MORTypes.Datastore)

        # Resource pool
        if not args.resource_pool:
            resource_pools = server.get_resource_pools()
            resource_pool_name = [k for k, v in resource_pools.items()
                                  if v == resource_pools.values()[0]][0]
        else:
            resource_pool_name = VIMor(args.resource_pool,
                                       MORTypes.ResourcePool)

        # Network
        if not args.network:
            network_name = 'VM Network'
        else:
            network_name = VIMor(args.network, MORTypes.Network)

        ovf = lib.get_descriptor(ovf_filepath)
        descriptor_info = lib.parse_descriptor(ovf, server)
        support_info = lib.validate_host(host_name, ovf, server)

        vm_names = args.vm_names
        for vm_name in vm_names:
            if server.get_vm_by_name(vm_name):
                print 'Already Exists VM.'
            else:
                # New VM name
                vapp_name = vm_name

                # Create spec
                import_spec = lib.create_import_spec(resource_pool_name,
                                                     datastore_name,
                                                     ovf, vapp_name,
                                                     host=host_name,
                                                     network=network_name,
                                                     server=server)

                if hasattr(import_spec, "Warning"):
                    print "Warning", import_spce.Warning[0].LocalizedMessage

                http_nfc_lease = lib.import_vapp(resource_pool_name,
                                                 import_spec,
                                                 host=host_name,
                                                 server=server)

                # Http request
                lib.lease(http_nfc_lease, ovf_filepath, server)

                print '%s Done.' % vm_name

    finally:
        # Remove
        if os.path.exists(download_temp):
            print 'Remove download temporary files...'
            shutil.rmtree(download_temp)
        if os.path.exists(extract_temp):
            shutil.rmtree(extract_temp)
