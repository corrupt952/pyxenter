# -*- coding: utf-8 -*-


def download_file(url, directory_path):
    u"""Downloading file

    @param url            URL
    @param directory_path Saving file path.

    @return Download file path.
    """
    # Import
    import os
    import urlparse
    import urllib

    if os.path.exists(directory_path):
        os.mkdir(directory_path)
    filename = urlparse.urlparse(url)[2].split('/')[-1]
    file_path = os.path.join(directory_path, filename)
    print 'Donwloading...'

    def progress(block_count, block_size, total_size):
        u"""Download animation

        @param block_count Download file block count
        @param block_size  Download file block size
        @param total_size  Download file total size
        """
        percentage = 100.0 * block_count * block_size / total_size
        sys.stdout.write('[')
        for i in range(50):
            if percentage <= (i + 1) * 2:
                sys.stdout.write(' ')
            else:
                sys.stdout.write('#')
        sys.stdout.write(']')
        print " %.0f %% (%d KB)\r" % (percentage, total_size / 1024),

    urllib.urlretrieve(
        url=url,
        filename=file_path,
        reporthook=progress)

    print
    print 'Done.'
    return file_path


def ova_extract(ova_path, directory_path):
    u"""Extract OVA file

    @param ova_path       OVA file path.
    @param directory_path Saving file of directory path.

    @return Extract OVA file path.
    """
    # Import
    import os
    import tarfile

    if os.path.exists(directory_path):
        os.mkdir(directory_path)

    tar_file = tarfile.open(ova_path)
    print "Extracting..."
    tar_file.extractall(directory_path)
    tar_file.close()
    for filename in os.listdir(directory_path):
        if filename.find('.ovf') > 0:
            return os.path.join(os.path.dirname(directory_path), filename)
    print "OVA file extract error."
    sys.exit()


def check_ovf(ovf_path):
    u"""Replace text.

    Replace ... vmware.cdrom.iso -> vmware.cdrom.atapi

    @param file_path OVF file path
    """
    print 'Check OVF file...'
    ovf_file = open(ovf_path, 'r')
    ovf_text = ovf_file.read()
    ovf_file.close()
    ovf_file = open(ovf_path, 'w')
    ovf_file.write(ovf_text.replace('vmware.cdrom.iso', 'vmware.cdrom.atapi'))
    ovf_file.close()


def get_descriptor(ovf_path):
    u"""Getting data in OVF file.

    @ovf_path OVF file path

    @return   Data in OVF file.
    """
    fh = open(ovf_path, "r")
    ovf_descriptor = fh.read()
    fh.close()
    return ovf_descriptor


def parse_descriptor(ovf_descriptor, server):
    u"""Exploding Data in OVF file.

    @param ovf_descriptor Data in OVF file.
    @param server         Instance of VIServer

    @return Data in OVF File
    """
    # Import
    from pysphere.resources import VimService_services as VI

    ovf_manager = server._do_service_content.OvfManager
    request = VI.ParseDescriptorRequestMsg()
    _this = request.new__this(ovf_manager)
    _this.set_attribute_type(ovf_manager.get_attribute_type())
    request.set_element__this(_this)
    request.set_element_ovfDescriptor(ovf_descriptor)
    pdp = request.new_pdp()
    pdp.set_element_locale("")
    pdp.set_element_deploymentOption("")
    request.set_element_pdp(pdp)
    return server._proxy.ParseDescriptor(request)._returnval


def validate_host(host_name, ovf_descriptor, server):
    u"""Analysis OVF file.

    @param host_name      Host name
    @param ovf_descriptor Data in OVF file
    @param server         Instance of VIServer

    @return Result of analysed OVF file.
    """
    # Import
    from pysphere.resources import VimService_services as VI

    hosts = server.get_hosts()
    host = [k for k, v in hosts.items() if v == host_name][0]
    if not host:
        raise ValueError("invalid ESX host name")
    ovf_manager = server._do_service_content.OvfManager
    request = VI.ValidateHostRequestMsg()
    _this = request.new__this(ovf_manager)
    _this.set_attribute_type(ovf_manager.get_attribute_type())
    request.set_element__this(_this)
    request.set_element_ovfDescriptor(ovf_descriptor)
    h = request.new_host(host)
    h.set_attribute_type(host.get_attribute_type())
    request.set_element_host(h)
    vhp = request.new_vhp()
    vhp.set_element_locale("")
    vhp.set_element_deploymentOption("")
    request.set_element_vhp(vhp)
    return server._proxy.ValidateHost(request)._returnval


def find_datastore_by_name(datastore_name, server):
    u"""Finding DataStore by DataStore name.

    @param datastore_name DataStore name
    @param server         Instance of VIServer

    @return DataStore
    """
    # Import
    from pysphere import VIProperty

    ret = None
    for dc in server._get_datacenters().values():
        dc_properties = VIProperty(server, dc)
        for ds in dc_properties.datastore:
            if ds.name == datastore_name:
                ret = ds._obj
                break
        if ret:
            break
    if not ret:
        raise ValueError("Couldn't find datastore '%s'" % (datastore_name))
    return ret


def find_network_by_name(network_name, server):
    u"""Finding network by Network name.

    @param network_name Network name
    @param server       Instance of VIServer

    @return Network
    """
    # Import
    from pysphere import VIProperty

    ret = None
    for dc in server._get_datacenters().values():
        dc_properties = VIProperty(server, dc)
        for nw in dc_properties.network:
            if nw.name == network_name:
                ret = nw._obj
                break
        if ret:
            break
    if not ret:
        raise ValueError("Couldn't find network '%s'" % (network_name))
    return ret


def find_vmfloder_by_name(folder_name, server):
    u"""Finding Datacenter by Datacenter name.

    @param folder_name Datacenter name
    @param server      Instance of VIServer

    @return Datacenter
    """
    # Import
    from pysphere import VIProperty

    ret = None
    for dc in server._get_datacenters().values():
        dc_properties = VIProperty(server, dc)
        if dc_properties.vmFolder.name == folder_name:
            return dc_properties.vmFolder._obj
    raise ValueError("Couldn't find folder '%s'" % (folder_name))


def create_import_spec(resource_pool_mor,
                       datastore,
                       ovf_descriptor,
                       name,
                       host=None,
                       network=None,
                       ip_allocation_policy="fixedPolicy",
                       ip_protocol="IPv4",
                       disk_provisioning="flat",
                       server=None):
    u"""Create spec for VM.

    @param datastore            DataStore name
    @param ovf_descriptor       Data in OVF file
    @param name                 VM name
    @param host                 Host name
    @param network              Network name
    @param ip_allocation_policy IP address type(DHCP, etc...)
    @param ip_protocol          IP protocol
    @param disk_provisioning    Disk provision
    @param server               Instance of VIServer

    @return Spec for VM
    """
    # Import
    from pysphere import VIApiException
    from pysphere.resources import VimService_services as VI

    if not server:
        raise VIApiException('Not found server.')
    # get the host MOR
    if host:
        hosts = server.get_hosts()
        host = [k for k, v in hosts.items() if v == host][0]
        if not host:
            raise ValueError("invalid ESX host name")
    # get the network MOR:
    if network:
        network_mor = find_network_by_name(network, server)

    #get the datastore MOR
    datastore_mor = find_datastore_by_name(datastore, server)

    ovf_manager = server._do_service_content.OvfManager
    request = VI.CreateImportSpecRequestMsg()
    _this = request.new__this(ovf_manager)
    _this.set_attribute_type(ovf_manager.get_attribute_type())
    request.set_element__this(_this)

    request.set_element_ovfDescriptor(ovf_descriptor)

    rp = request.new_resourcePool(resource_pool_mor)
    rp.set_attribute_type(resource_pool_mor.get_attribute_type())
    request.set_element_resourcePool(rp)

    ds = request.new_datastore(datastore_mor)
    ds.set_attribute_type(datastore_mor.get_attribute_type())
    request.set_element_datastore(ds)

    cisp = request.new_cisp()
    cisp.set_element_entityName(name)
    cisp.set_element_locale("")
    cisp.set_element_deploymentOption("")
    if host:
        h = cisp.new_hostSystem(host)
        h.set_attribute_type(host.get_attribute_type())
        cisp.set_element_hostSystem(h)
    if network:
        network_mapping = cisp.new_networkMapping()
        network_mapping.set_element_name(network)
        n_mor = network_mapping.new_network(network_mor)
        n_mor.set_attribute_type(network_mor.get_attribute_type())
        network_mapping.set_element_network(n_mor)

        network_mapping2 = cisp.new_networkMapping()
        network_mapping2.set_element_name("Internal")
        n_mor = network_mapping.new_network(network_mor)
        n_mor.set_attribute_type(network_mor.get_attribute_type())
        network_mapping2.set_element_network(n_mor)

        cisp.set_element_networkMapping([network_mapping, network_mapping2])

    if ip_allocation_policy:
        cisp.set_element_ipAllocationPolicy(ip_allocation_policy)
    if ip_protocol:
        cisp.set_element_ipProtocol(ip_protocol)
    if disk_provisioning:
        cisp.set_element_diskProvisioning(disk_provisioning)

    request.set_element_cisp(cisp)
    return server._proxy.CreateImportSpec(request)._returnval


def import_vapp(resource_pool, import_spec,
                host=None, folder=None, server=None):
    u"""Deploy VM

    @param resource_pool  Resource Pool name
    @param import_spec    Spec for VM
    @param host           Host name
    @param folder         DataCenter name
    @param server         Instance of VIServer
    """
    # Import
    from pysphere.resources import VimService_services as VI

    if not server:
        raise VIApiException('Not found server.')

    # hostがNoneでなければ取得してくる
    if host:
        hosts = server.get_hosts()
        host = [k for k, v in hosts.items() if v == host][0]
        if not host:
            raise ValueError("invalid ESXi host name")

    #get the vm folder MOR
    if folder:
        folder = find_vmfolder_by_name(folder)
    request = VI.ImportVAppRequestMsg()
    _this = request.new__this(resource_pool)
    _this.set_attribute_type(resource_pool.get_attribute_type())
    request.set_element__this(_this)
    request.set_element_spec(import_spec.ImportSpec)
    if host:
        h = request.new_host(host)
        h.set_attribute_type(host.get_attribute_type())
        request.set_element_host(h)
    if folder:
        f = request.new_folder(folder)
        f.set_attribute_type(folder.get_attribute_type())
        request.set_element_folder(f)
    return server._proxy.ImportVApp(request)._returnval


def get_vm_index(server, name):
    u"""Return index of Target VM in VM List

    If not exists VM, return -1.
    Othwerwise return Nutural number.
    @param server Instance of VIServer
    @param name   Target VM name

    @return Index
    """
    vm_names = get_vm_names(server)
    for n, vm_name in enumerate(vm_names):
        if vm_name == name:
            return n
    return -1


def get_vm_names(server):
    u"""Getting VM name List

    @param server Instacnce of VIServer

    @return List of the server has any VM name.
    """
    vm_paths = server.get_registered_vms()
    vm_names = []
    for vm_path in vm_paths:
        vm = server.get_vm_by_path(vm_path)
        vm_names.append(vm.get_property('name'))
    return vm_names


def lease(http_nfc_lease, ovf_file_path, server):
    u"""Uploading request files.

    @param http_nfc_lease Lease
    @param server         Insrance of VIServer
    """
    # Import
    import time
    import threading
    from pysphere import VIProperty
    from pysphere.resources import VimService_services as VI

    go_on = True
    lease = VIProperty(server, http_nfc_lease)
    while lease.state == 'initializing':
        print lease.state
        lease._flush_cache()
    if lease.state != 'ready':
        print "something went wrong"
        exit()

    def keep_lease_alive(lease):
        u"""プロセスを継続させる

        @param leaese 仮のVM
        """
        request = VI.HttpNfcLeaseProgressRequestMsg()
        _this = request.new__this(lease)
        _this.set_attribute_type(lease.get_attribute_type())
        request.set_element__this(_this)
        request.set_element_percent(50)
        while go_on:
            server._proxy.HttpNfcLeaseProgress(request)

    time.sleep(5)
    t = threading.Thread(target=keep_lease_alive, args=(http_nfc_lease,))
    t.start()

    # Upload
    print 'Uploading...'
    upload_format_file(lease, '.vmdk', ovf_file_path, server)

    go_on = False
    t.join()

    request = VI.HttpNfcLeaseCompleteRequestMsg()
    _this = request.new__this(http_nfc_lease)
    _this.set_attribute_type(http_nfc_lease.get_attribute_type())
    request.set_element__this(_this)
    server._proxy.HttpNfcLeaseComplete(request)


def upload_format_file(lease, format, ovf_file_path, server):
    u"""If any file matching file format, Upload Serber.

    @param lease  Lease
    @param format File format
    @param server Instance of VIServer
    """
    # Import
    import os
    import urlparse
    import urllib2
    import mmap

    # ここでファイル一覧を取得
    for dev_url in lease.info.deviceUrl:
        filenames = os.listdir(os.path.dirname(ovf_file_path))
        for filename in filenames:
            # ファイルの拡張子がvmdkであった場合、アップロードを開始する
            if filename.find(format) > 0:
                host = urlparse.urlparse(server._proxy.binding.url)
                hostname = host.hostname
                upload_url = dev_url.url.replace("*", hostname)
                #  ここでfilenameにOVFファイルのディレクトリパスを付与する
                dir_path = os.path.dirname(ovf_file_path)
                filename = os.path.join(dir_path, filename)
                fsize = os.stat(filename).st_size
                f = open(filename, 'rb')
                mmapped_file = mmap.mmap(f.fileno(), 0,
                                         access=mmap.ACCESS_READ)
                request = urllib2.Request(upload_url, mmapped_file)
                request.add_header("Content-Type",
                                   "application/x-vnd.vmware-streamVmdk")
                request.add_header("Connection", "Keep-Alive")
                request.add_header("Content-Length", str(fsize))
                opener = urllib2.build_opener(urllib2.HTTPHandler)
                resp = opener.open(request)
                mmapped_file.close()
                f.close()


def powered_on(vm, server):
    u"""Powered on VM.

    @param vm     VM
    @param server Instance of VIServer
    """
    if vm.is_powered_off():
        print 'Powered on...'
        try:
            vm.power_on()
        except:
            raise Exception('Powered error.')
    else:
        print 'Already Powered On.'


def powered_off(vm, server):
    u"""Powered off VM.

    @param vm     VM
    @param server Instance og VIServer
    """
    if vm.is_powered_on():
        print 'Powered off...'
        try:
            vm.power_off()
        except:
            raise Exception('Powered error.')
    else:
        print 'Already Powered Off.'


def delete_vm_by_path(path, server, remove_files=True):
    """Delete VM

    Unregisters a VM and remove it files from the datastore by path.
    @path is the path to VM.
    @remove_files - if True (default) will delete VM files from datastore.
    """
    # Import
    from pysphere import VITask
    from pysphere.resources import VimService_services as VI

    try:
        #Get VM
        vm = server.get_vm_by_path(path)

        if remove_files:
            #Invoke Destroy_Task
            request = VI.Destroy_TaskRequestMsg()

            _this = request.new__this(vm._mor)
            _this.set_attribute_type(vm._mor.get_attribute_type())
            request.set_element__this(_this)
            ret = server._proxy.Destroy_Task(request)._returnval
            task = VITask(ret, server)

            #Wait for the task to finish
            status = task.wait_for_state([task.STATE_SUCCESS,
                                          task.STATE_ERROR])
            if status == task.STATE_SUCCESS:
                print "VM successfully unregistered and deleted from datastore"
            elif status == task.STATE_ERROR:
                print "Error removing vm:", task.get_error_message()
        elif not remove_files:
            #Invoke UnregisterVMRequestMsg
            request = VI.UnregisterVMRequestMsg()

            _this = request.new__this(vm._mor)
            _this.set_attribute_type(vm._mor.get_attribute_type())
            request.set_element__this(_this)
            ret = server._proxy.UnregisterVM(request)
            task = VITask(ret, server)

            print "Done."

    except (VI.ZSI.FaultException), e:
        raise VIApiException(e)


def delete_vm_by_name(name, server, remove_files=True):
    """Delete VM

    Unregisters a VM and remove it files from the datastore by name.
    @name is the VM name.
    @remove_files - if True (default) will delete VM files from datastore.
    """
    # Import
    from pysphere import VITask
    from pysphere.resources import VimService_services as VI

    try:
        #Get VM
        vm = server.get_vm_by_name(name)

        if remove_files:
            #Invoke Destroy_Task
            request = VI.Destroy_TaskRequestMsg()

            _this = request.new__this(vm._mor)
            _this.set_attribute_type(vm._mor.get_attribute_type())
            request.set_element__this(_this)
            ret = server._proxy.Destroy_Task(request)._returnval
            task = VITask(ret, server)

            #Wait for the task to finish
            status = task.wait_for_state([task.STATE_SUCCESS,
                                          task.STATE_ERROR])
            if status == task.STATE_SUCCESS:
                print "VM successfully unregistered and deleted from datastore"
            elif status == task.STATE_ERROR:
                print "Error removing vm:", task.get_error_message()
        elif not remove_files:
            #Invoke UnregisterVMRequestMsg
            request = VI.UnregisterVMRequestMsg()

            _this = request.new__this(vm._mor)
            _this.set_attribute_type(vm._mor.get_attribute_type())
            request.set_element__this(_this)
            ret = server._proxy.UnregisterVM(request)
            task = VITask(ret, server)

            print "Done."

    except (VI.ZSI.FaultException), e:
        raise VIApiException(e)
