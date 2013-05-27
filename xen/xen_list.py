# coding: utf-8

# SHOW VMs METHOD #
def show_vm_list(args, session):
   u"""VMの一覧を表示する
   
   @param args    Commandline argumetn
   @param session Session
   """
   #Get VMs
   vms = session.xenapi.VM.get_all()
   
   print
   for vm in vms:
      record = session.xenapi.VM.get_record(vm)
      if not record["is_control_domain"] \
         and not 'Transfer' in record["name_label"] \
         and record["is_a_template"] == args.template :
     
         # Print VMs
         print "VM: %s"         % record['name_label']
         print "PowerState: %s" % record['power_state']
         print "Xen tools : %s" % ('Installed' \
                if record['guest_metrics'].split(':')[1] <> 'NULL' else 'Not installed.')
         print