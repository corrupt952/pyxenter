# -*- coding: utf-8 -*-


def args():
    u"""Set argument.

    @return argument
    """
    # from subcommands import
    import argparse
    from subcommands import list
    from subcommands import destroy
    from subcommands import deploy
    from subcommands import getip
    from subcommands import power

    # Parent parser
    parser = argparse.ArgumentParser(description='ESXi Tools')

    # Sub parser
    subparsers = parser.add_subparsers(help='commands')

    # List parser
    list.set_parsers(subparsers)

    # Destroy parser
    destroy.set_parsers(subparsers)

    # Deploy parser
    deploy.set_parsers(subparsers)

    # IP parser
    getip.set_parsers(subparsers)

    # Power parser
    power.set_parsers(subparsers)

    return parser.parse_args()
