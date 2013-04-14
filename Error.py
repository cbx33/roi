'''
Created on 13 Apr 2013

@author: pete
'''

#Config Errors
FileNotExist = 0
FileNotParsable = 1
WordIndexNotExist = 2
TransIndexNotExist = 3
MissingSection = 4
MissingOption = 5

#Index Errors
SourceDirectoryNotExist = 0

class ConfigError(Exception):
    def __init__(self, CEType, error=""):
        self.type = CEType
        if self.type == FileNotExist:
            self.val = "The ROI config file could not be found" 
        elif self.type == FileNotParsable:
            self.val = "The ROI config file is not parsable"
        elif self.type == WordIndexNotExist:
            self.val = "The WordIndex does not exist"
        elif self.type == TransIndexNotExist:
            self.val = "The TransIndex does not exist"
        elif self.type == MissingSection:
            self.val = error
        elif self.type == MissingOption:
            self.val = error
        else:
            self.val = "Undefined Error"

    def __str__(self):
        return repr(self.val)

class ROIIndexError(Exception):
    def __init__(self, CEType, error=""):
        self.type = CEType
        if self.type == SourceDirectoryNotExist:
            self.val = "The source directory could not be found" 
        else:
            self.val = "Undefined Error"

    def __str__(self):
        return repr(self.val)

