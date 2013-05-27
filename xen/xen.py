# coding: utf-8

# MAIN #
def main():
    # Import
    import getpass
    import socket
    import sys
    
    import xen_argument
    import XenAPI
    
    # Get argument
    args = xen_argument.args()
    
    # Set URL, Username, Password
    url    = raw_input('URL> ')  if args.url    == None else args.url
    user   = raw_input('User> ') if args.user   == None else args.user
    passwd = getpass.getpass()   if args.passwd == None else args.passwd
    
    session = None
    try:
        print 'Making session...'
        session = XenAPI.Session(url)
        print 'Connecting...'
        session.login_with_password(user,passwd)
       
        #Execute function
        args.func(args, session)
    except socket.error:
        print >> sys.stderr, 'Not found server.'
    except Exception, e:
        print >> sys.stderr, e.message
    finally:
        if session <> None:
            print 'Removing session...'
            session.logout()

if __name__ == '__main__':
    main()