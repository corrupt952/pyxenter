#!/usr/bin/env python
# coding: utf-8


def main():
    u"""Main method

    Create session.
    Excute subcommand.
    """
    import getpass
    import socket
    import sys

    from subcommands import argument
    import XenAPI

    # Get argument
    args = argument.args()

    # Set URL, Username, Password
    url = args.url if args.url else raw_input('URL> ')
    user = args.user if args.user else raw_input('User> ')
    passwd = args.passwd if args.passwd else getpass.getpass()

    try:
        print 'Making session...'
        session = XenAPI.Session(url)
    except socket.error:
        print >> sys.stderr, 'Not found server.'
        sys.exit(1)

    try:
        print 'Connecting...'
        session.login_with_password(user, passwd)

        #Execute function
        args.func(args, session)
    except Exception, e:
        print >> sys.stderr, e.message
    finally:
        print 'Removing session...'
        session.logout()


if __name__ == '__main__':
    main()
