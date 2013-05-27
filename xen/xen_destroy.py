# coding: utf-8

def destroy(args, session):
   u"""Destroying VM
   
   @param args    Commandline argument
   @param session Session
   """
   # Import
   import sys
   import xen_lib
   
   # Set VM name
   vm = xen_lib.get_vm(vm_name, session)
   if not vm == None:
      try:
         print 'Destroying...'
         vdis = xen_lib.get_storage_vdis(vm, session)
         for vdi in vdis:
            session.xenapi.VDI.destroy(vdi)
         session.xenapi.VM.destroy(vm)
         print 'Done.'
      except:
         print >> sys.stderr, 'Please shutdown for VM.'
   else:
      print >> sys.stderr, 'Not found VM.'