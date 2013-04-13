'''
Created on 13 Apr 2013

@author: pete
'''

import re
import operator
import json
import os.path

class Search():
    
    class Result():
        
        def __init__(self, slang, dlang, iid, slangResult, dlangResult, project):
            self.slang = slang
            self.dlang = dlang
            self.iid = iid
            self.slangResult = slangResult
            self.dlangResult = dlangResult
            self.project = project
    
    def __init__(self, term, slang, dlang, config):
        print "Creating Search Object"
        self.term = term
        self.slang = slang
        self.dlang = dlang
        self.config = config
        
        pattern = re.compile('[^a-zA-Z0-9 ]+')
        self.words = pattern.sub('', self.term).split(" ")
        self.collectResults()
        self.sortResults()
        
    def collectResults(self):
        self.results = []
        for word in self.words:
            if len(word)>1:
                wlower = word.lower()
            try:
                wordFile = os.path.join(self.config.wordIndex, self.slang, wlower[0:2], wlower[0:2])
                f = open(wordFile)
                data = json.load(f)
                transIndexList = data[wlower]
            except:
                transIndexList = ""
        
            for transIndex in transIndexList:
                if transIndex != "":
                    for num in transIndexList[transIndex]:
                        self.results.append(transIndex+","+str(num))
        
    def sortResults(self):        
        self.nresults = {}
        for result in self.results:
            if self.nresults.has_key(result):
                self.nresults[result] += 1
            else:
                self.nresults[result] = 1
        
        self.sortedResults = sorted(self.nresults.iteritems(), key=operator.itemgetter(1))
        
    def returnResults(self):
        resultSet = []
        for entry in self.sortedResults[::-1][0:5]:
            sub_entry = entry[0].split(",")
            packFile = str(int(sub_entry[1])-(int(sub_entry[1])%self.config.packSize))
            destFilename = os.path.join(self.config.transIndex, sub_entry[0], self.dlang, packFile)
            sourceFilename = os.path.join(self.config.transIndex, sub_entry[0], self.slang, packFile)
            iid = sub_entry[1]
            project = sub_entry[0]

            try:
                sourceFileHandle = open(sourceFilename)
                destFileHandle = open(destFilename)
            except IOError:
                continue

            slangJSON = json.load(sourceFileHandle)
            dlangJSON = json.load(destFileHandle)

            sourceFileHandle.close()
            destFileHandle.close()

            slangResult = slangJSON[iid]
            dlangResult = dlangJSON[iid]

            resultInstance = self.Result(self.dlang, self.slang, sub_entry[1], slangResult, dlangResult, project)
            resultSet.append(resultInstance)

        return resultSet