# -*- coding: utf-8 -*-

# DEPLOY METHOD #
def deploy_vm(args, server):
    u"""Deploy VM(import)
  
    @param args   Commandline argument
    @param server Instance of VIServer
    """
    # Import 
    import os
    import sys
    import shutil
    from pysphere import VIMor
    import esxi_lib
    
    download_temp = './temp/'
    extract_temp = None
    try:
        # Download
        if not args.file_url == None:
            if args.file_url.find('.ova') > 0: 
                args.file_path = esxi_lib.download_file(args.file_url, download_temp)
            else:
                print >> sys.stderr , 'File format not supported.'
                exit()
        
        file_path = raw_input('OVF or OVA file path> ') if args.file_path == None else args.file_path
        if os.path.exists(file_path) == False:
            print "File not found."
            exit()
    
        if file_path.find('.ova') > 0:
            #  If  file format is ova
            extract_temp = r"./%s/" % file_path.split('/')[-1].replace('.ova', '')
            file_path = esxi_lib.ova_extract(file_path, extract_temp)
        elif file_path.find('.ovf') < 0:
            # If file format isn't ova and ovf
            print "File format not supported."
            exit()
        
        # ovf_file_path path
        ovf_file_path = file_path
        esxi_lib.check_ovf(ovf_file_path)
        
        # Remove mf File
        MF_FILE = ovf_file_path.replace('.ovf','.mf')
        if os.path.exists(MF_FILE):
            os.remove(MF_FILE)
        
        # New VM name
        vapp_name = raw_input('New VM name> ') if args.vm_name == None else args.vm_name
        
        # Host
        if args.datacenter == None:
            host_name = server.get_hosts().values()[0]
        else:
            host_name = VIMor(args.datacenter, MORTypes.Datacenter)
    
        # Datastore
        if args.datastore == None:
            datastore_name = server.get_datastores().values()[0]
        else:
            datastore_name = VIMor(args.datastore, MORTypes.Datastore)
        
        # Resource pool
        if args.resource_pool == None:
            resource_pool_name = [k for k,v in server.get_resource_pools().items()
                                            if v == server.get_resource_pools().values()[0]][0]
        else:
            resource_pool_name = VIMor(args.resource_pool, MORTypes.ResourcePool)
        
        # Network
        if args.network == None:
            network_name = 'VM Network'
        else:
            network_name = VIMor(args.network, MORTypes.Network)
        
        
        ovf = esxi_lib.get_descriptor(ovf_file_path)
        descriptor_info = esxi_lib.parse_descriptor(ovf, server)
        support_info = esxi_lib.validate_host(host_name, ovf, server)
        
        # Create spec
        import_spec = esxi_lib.create_import_spec(resource_pool_name, datastore_name,
                                                ovf,                vapp_name,
                                                host = host_name,   network = network_name,
                                                server = server)
    
        if hasattr(import_spec, "Warning"):
            print "Warning", import_spce.Warning[0].LocalizedMessage
        
        http_nfc_lease = esxi_lib.import_vapp(resource_pool_name, import_spec, host = host_name, server = server)
        
        # Http request
        esxi_lib.lease(http_nfc_lease, ovf_file_path, server)
    finally:
        # Remove
        if os.path.exists(download_temp) == True:
            print 'Remove download temporary files...'
            shutil.rmtree(download_temp)
        if os.path.exists(extract_temp) == True:
            shutil.rmtree(extract_temp)