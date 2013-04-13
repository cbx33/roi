'''
Created on 13 Apr 2013

@author: pete
'''

import ConfigParser
import os.path
import Error
import sys

class ROIIndexer:
    
    def __init__(self, configFileName):
        self.config = self.Config(configFileName)

    class Config():

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
                return False
            successfulConfig = self.config.read(configFileName)
            if successfulConfig == []:
                raise Error.ConfigError(Error.FileNotParsable)
                return False
        
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
        
if __name__ == "__main__":
    index = ROIIndexer('roi.cfg')