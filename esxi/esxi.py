#!/usr/bin/env python
# coding: utf-8

# MAIN #
def main():
    # Import
    import socket
    import getpass
    import sys
    from pysphere import VIApiException, VIServer
    import esxi_argument
    
    # Get argument
    args = esxi_argument.args()
    s = VIServer()
    
    # Set information
    host = raw_input('Host> ') if args.host   == None else args.host
    user = raw_input('User> ') if args.user   == None else args.user
    passwd = getpass.getpass('Password> ') if args.passwd == None else args.passwd
    try:
        print 'Connecting...'
        s.connect(host,user,passwd)
       
        # Execute function
        args.func(args, s)
    except socket.error:
        print >> sys.stderr, "Cannot connected."
    except VIApiException:
        print >> sys.stderr, "Incorrect user name or password."
    except Exception, e:
        print >> sys.stderr, e.message
    finally:
        if s.is_connected() == True:
            print 'Disconnecting...'
            s.disconnect()

if __name__ == '__main__':
    main()