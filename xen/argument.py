# -*- coding: utf-8 -*-

def args():
    u"""Set argument
    
    @return argument
    """
    # Import
    import argparse
    from subcommands import list
    from subcommands import destroy
    from subcommands import install
    from subcommands import power
    from subcommands import getip
   
    # Parent parser
    parser = argparse.ArgumentParser(description='Xen tool')
   
    # Sub parsers
    subparsers = parser.add_subparsers(help='commands.')
   
    # List parser
    list.set_parsers(subparsers)
    
    # Destroy parser
    destroy.set_parsers(subparsers)
    
    # Install parser(use template)
    install.set_parsers(subparsers)
    
    # Power parser
    power.set_parsers(subparsers)
    
    # Get IP Parser
    getip.set_parsers(subparsers)
    
    # Return
    return parser.parse_args()