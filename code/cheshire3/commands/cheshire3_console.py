"""Interact with Cheshire3."""

import sys
import os

from code import InteractiveConsole

from cheshire3.internal import cheshire3Version
from cheshire3.commands.cmd_utils import Cheshire3ArgumentParser

class Cheshire3Console(InteractiveConsole):
    """Cheshire3 Interactive Console."""
    
    def __init__(self, args, locals=None, filename="<console>"):
        InteractiveConsole.__init__(self, locals, filename)
        init_code_lines = [
           'from cheshire3.session import Session',
           'from cheshire3.server import SimpleServer',
           'session = Session()',
           'server = SimpleServer(session, "{}")'.format(args.serverconfig),
        ]
        # Seed console with standard initialization code
        for line in init_code_lines:
            self.push(line)
            
    def interact(self, banner=None):
        """Emulate the standard interactive Python console.
        
        The optional banner argument specify the banner to print
        before the first interaction; by default it prints a banner
        similar to the one printed by the real Python interpreter.
        """
        if banner is None:
            c3_version = '.'.join([str(p) for p in cheshire3Version])
            banner = """Python {} on {}
Cheshire3 {} Interactive Console
Type "help", "copyright", "credits" or "license" for more information.\
""".format(sys.version, sys.platform, c3_version)
#            banner = "Cheshire3 {} Interactive Console""".format(c3_version)
        return InteractiveConsole.interact(self, banner)
        

def main(argv=None):
    """Main method for cheshire3 command."""
    global argparser, session, server, db
    if argv is None:
        args = argparser.parse_args()
    else:
        args = argparser.parse_args(argv)
    console = Cheshire3Console(args)
    # Standard Cheshire3 initialization code
    if args.database is not None:
        dbline = 'db = server.get_object(session, "{}")'.format(args.database)
        console.push(dbline)
    
    console.interact()
    return 0


argparser = Cheshire3ArgumentParser()
#subparsers = argparser.add_subparsers(title='subcommands',
#                                   description='valid subcommands')
session = None
server = None
db = None
   
if __name__ == '__main__':
    main(sys.argv)