#!/usr/bin/env python
# coding: utf-8


def main():
    u"""Main method

    Create session.
    Excute subcommand.
    """
    # Import
    import socket
    import getpass
    import sys
    from pysphere import VIApiException, VIServer
    from subcommands import argument

    # Get argument
    args = argument.args()
    s = VIServer()

    # Set information
    host = args.host if args.host else raw_input('Host> ')
    user = args.user if args.user else raw_input('User> ')
    passwd = args.passwd if args.passwd else getpass.getpass('Password> ')
    try:
        print 'Connecting...'
        s.connect(host, user, passwd)

        # Execute function
        args.func(args, s)
    except socket.error:
        print >> sys.stderr, "Cannot connected."
    except VIApiException:
        print >> sys.stderr, "Incorrect user name or password."
    except Exception, e:
        print >> sys.stderr, e.message
    finally:
        if s.is_connected():
            print 'Disconnecting...'
            s.disconnect()


if __name__ == '__main__':
    main()
