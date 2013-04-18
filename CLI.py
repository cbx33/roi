'''
Created on 13 Apr 2013

@author: pete
'''
from optparse import OptionParser, OptionGroup
import sys



class CLIParser:
    def __init__(self):
        description = "Indexer"
        usage = "Usage: %prog <CFG_FILE>"
        epilog = "Constructive comments and feedback gladly accepted."
        version = "%prog version 0.1"
        
        parser = OptionParser(usage=usage, description=description, epilog=epilog, version=version)
        parser.add_option('--cfg', dest='cfg_file', metavar='<cfg_file>', help='Configuration file.')
        group = OptionGroup(parser, "Search options")
        group.add_option('--search', dest="search", action="store_true", default=False, help='Activates the search context.')
        group.add_option('-q', '--query', dest='query', help='The term to use in your query.')
        group.add_option('-o', '--origin', dest='origin', default='en_US.po', help='The original language file to use in your query.')
        group.add_option('-t', '--target', dest='target', help='The target language file to perform your search.')
        parser.add_option_group(group)

        group = OptionGroup(parser, "Full indexing options")
        group.add_option('--full-index', dest="fullIndex", action="store_true", default=False, help='Activates the full index context. (Will not run unless indexing directories are empty.)')
        group.add_option('-s', '--source-dir', dest='sourceDir', help='The source directory for all projects')
        parser.add_option_group(group)

        group = OptionGroup(parser, "Single project indexing options")
        group.add_option('--project-index', dest="partialIndex", action="store_true", default=False, help='Activates the single project context. (This will destroy a projects existing index)')
        group.add_option('-p', '--project-dir', dest='projectDir', help='The project directory for a specific project')
        parser.add_option_group(group)

        # Verify arguments
        (opts, args) = parser.parse_args()

        contextCount = 0
        for context in ["source", "fullIndex", "partialIndex"]:
            if context in dir(opts):
                if getattr(opts, context):
                    contextCount += 1
        
        if contextCount == 0 or contextCount > 1:
            print "You must choose one context at least, but not several!"
            sys.exit(0)
        
        """
        # A configuration file is required
        if not opts.cfg_file:
            print "Please provide a configuration file."
            parser.print_help()
            sys.exit(-1)
        
        # Don't allow queries for empty strings
        if not opts.query or len(opts.query) == 0:
            print "Please provide a valid string to perform your query."
            parser.print_help()
            sys.exit(-1)
        
        # Make sure that a target language file is provided
        if not opts.target:
            print "A target language file is required."
            parser.print_help()
            sys.exit(-1)
        """

        self.opts = opts
        self.args = args
    
    def returnOptions(self):
        return self.opts