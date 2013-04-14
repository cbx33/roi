'''
Created on 14 Apr 2013

@author: pete
'''

#TODO - Need to make it not rely on en_GB.po for indexing, 
#       will use msgid instead.
#TODO - Split out the pod function into a separate function
#TODO - Make the word indexer reusable for partial indexing
#TODO - Make the project indexer reusable for partial indexing
#TODO - Search for languages, not a list :p

import polib
import re
import os
import os.path
import json
import Error

class Index():
    def __init__(self, config):
        self.config = config
        self.wordIndex = self.config.wordIndex
        self.transIndex = self.config.transIndex
        self.packSize = self.config.packSize

    def fullIndex(self, source):
        self.source = source
        if not os.path.exists(self.source):
            raise Error.ROIIndexError(Error.SourceDirectoryNotExist)

        if not os.listdir(self.transIndex) == []:
            raise Error.ROIIndexError(Error.TransIndexNotEmpty)
        if not os.listdir(self.wordIndex) == []:
            raise Error.ROIIndexError(Error.WordIndexNotEmpty)
        
        for projectName in os.listdir(self.source):
            projectInstance = self.Project(projectName, self.transIndex, self.wordIndex, self.packSize, self.source)
            projectInstance.indexProject()

    class Project():
        def __init__(self, project, transIndex, wordIndex, packSize, source):
            self.project = project
            self.source = source
            self.wordIndex = wordIndex
            self.transIndex = transIndex
            self.packSize = packSize
            self.pattern = re.compile('[^a-zA-Z0-9 ]+')
            self.projTransIndex = os.path.join(self.transIndex, self.project)
        
        def indexProject(self):
            self.windex = {}
            self.id_database = {}
            self.indexmeta = {}
            self.index = 0
            
            self.projectDir = os.path.join(self.source, self.project)
            
            #This is nasty right now, but necessary as the indexer NEEDS en_GB to be first
            podlist = os.listdir(self.projectDir)
            if "en_GB.po" in podlist:
                podlist.remove("en_GB.po")
            podlist = ["en_GB.po"] + podlist
            
            for pod in podlist:
                self.indexProjectLanguage(pod)
        
            for pod in self.indexmeta:
                for p in range(0, len(self.indexmeta[pod]), self.packSize):
                    f = open(self.projTransIndex+"/"+pod+"/"+str(p),"w")
                    todump = {}
                    for a in range(p, p+self.packSize):
                        try:
                            todump[a] = self.indexmeta[pod][a]
                        except KeyError:
                            if p < len(self.indexmeta[pod]):
                                continue
                            else:
                                break
                    json.dump(todump, f)
                    f.close()

            for pod in self.windex:
                for pair in self.windex[pod]:
                    odir = self.wordIndex+"/"+pod+"/"+pair
                    if not os.path.exists(odir):
                        os.makedirs(odir)
        
                    if os.path.exists(self.wordIndex+"/"+pod+"/"+pair+"/"+pair):
                        f = open(self.wordIndex+"/"+pod+"/"+pair+"/"+pair)
                        old_windex = json.load(f)
                        f.close()
        
                        for word in self.windex[pod][pair]:
                            if old_windex.has_key(word):
                                old_windex[word][self.project] = self.windex[pod][pair][word][self.project]
                            else:
                                old_windex[word] = self.windex[pod][pair][word]
                        
                        f = open(self.wordIndex+"/"+pod+"/"+pair+"/"+pair, "w")
                        json.dump(old_windex, f)
                        f.close()
                    else:
                        f = open(odir+"/"+pair, "w")
                        json.dump(self.windex[pod][pair], f)
                        f.close()
                        
        def indexProjectLanguage(self, pod):
            self.indexmeta[pod] = {}
            self.windex[pod] = {}
            projectLangTransIndex = self.projTransIndex+"/"+pod

            if not os.path.exists(projectLangTransIndex):
                os.makedirs(projectLangTransIndex)
            print pod
            print self.projectDir+"/"+pod
            po = polib.pofile(self.projectDir+"/"+pod)
            
            for entry in po.translated_entries():
                # entry.msgid, entry.msgstr
                sanitised = self.pattern.sub(' ', entry.msgstr)
                words = self.pattern.sub('', sanitised).split(" ")

                key = ",".join(map(lambda x:",".join(x), entry.occurrences))

                if pod == "en_GB.po":
                    self.id_database[key] = [self.index, entry.msgid]

                for word in words:
                    if len(word)>1:
                        wlower = word.lower()
                        pair = wlower[0:2]
                        
                        if not self.windex[pod].has_key(pair):
                            self.windex[pod][pair] = {wlower:{self.project:[]}}
                        else:
                            if not self.windex[pod][pair].has_key(wlower):
                                self.windex[pod][pair][wlower] = {self.project:[]}
                        try:
                            self.windex[pod][pair][wlower][self.project].append(self.id_database[key][0])
                        except KeyError:
                            continue

                try:
                    ourindex = str(self.id_database[key][0])
                    self.indexmeta[pod][int(ourindex)] = entry.msgstr
                except KeyError:
                    continue

                self.index += 1
