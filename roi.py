'''
Created on 13 Apr 2013

@author: pete
'''

import ConfigParser
import os.path
import Error
import sys
import Search
from optparse import OptionParser

class ROIIndexer(object):
    
    def __init__(self, configFileName):
        self.config = self.Config(configFileName)

    def search(self, term, slang, dlang):
        SearchObject = Search.Search(term, slang, dlang, self.config)
        results = SearchObject.returnResults()
        for result in results:
            print "================="
            print result.project + "-" + result.iid
            print "-----------------"
            print result.slangResult
            print "-----------------"
            print result.dlangResult
        print "================="

    class Config(object):

        def __init__(self, configFileName):
            try:
                self.getConfig(configFileName)
                self.checkConfig()
            except Error.ConfigError as e:
                print e.val
                sys.exit(0)
            
        def getConfig(self, configFileName):
            self.config = ConfigParser.SafeConfigParser()
            if not os.path.exists(configFileName):
                raise Error.ConfigError(Error.FileNotExist)

            successfulConfig = self.config.read(configFileName)
            if successfulConfig == []:
                raise Error.ConfigError(Error.FileNotParsable)
        
        def checkConfig(self):
            try:
                self.wordIndex = self.config.get('Main', 'WordIndex')
                if not os.path.isdir(self.wordIndex):
                    raise Error.ConfigError(Error.WordIndexNotExist)
                
                self.transIndex = self.config.get('Main', 'TransIndex')
                if not os.path.isdir(self.transIndex):
                    raise Error.ConfigError(Error.TransIndexNotExist)
        
                self.packSize = self.config.getint('Main', 'packSize')
                
                #At the moment overriding this setting
                if self.packSize != 100:
                    self.packSize = 100
            except ConfigParser.NoOptionError as e:
                raise Error.ConfigError(Error.MissingOption, e)
            except ConfigParser.NoSectionError as e:
                raise Error.ConfigError(Error.MissingSection, e)

def main():

    description = "Indexer"
    usage = "Usage: %prog <CFG_FILE>"
    epilog = "Constructive comments and feedback gladly accepted."
    version = "%prog version 0.1"

    parser = OptionParser(usage=usage, description=description, epilog=epilog, version=version)
    parser.add_option('--cfg', dest='cfg_file', metavar='<cfg_file>', help='Configuration file.')
    parser.add_option('-q', '--query', dest='query', help='The term to use in your query.')
    parser.add_option('-o', '--origin', dest='origin', default='en_US.po', help='The original language file to use in your query.')
    parser.add_option('-t', '--target', dest='target', help='The target language file to perform your search.')

    # Verify arguments
    (opts, args) = parser.parse_args()

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
        
    index = ROIIndexer(opts.cfg_file)
    index.search(opts.query, opts.origin, opts.target)
    
if __name__ == "__main__":
    main()
