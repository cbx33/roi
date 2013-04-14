'''
Created on 14 Apr 2013

@author: pete
'''

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

    def fullIndex(self, source):
        self.source = source
        if not os.path.exists(self.source):
            raise Error.ROIIndexError(Error.SourceDirectoryNotExist)

        indir = self.source
        outdir = self.config.wordIndex
        outdirmeta = self.config.transIndex
        index_lim = self.config.packSize
        
        windex = {}
        
        tot = 0
        for project in os.listdir(indir):
            id_database = {}
            indexmeta = {}
            index = 0
            if "." not in project:    
                pos = ['en_GB.po','de.po','fr.po','as.po','az.po','be.po','cs.po','dz.po','ja.po']
                for pod in pos:
                    indexmeta[pod] = {}
                    windex[pod] = {}
        
                    if not os.path.exists(outdirmeta+"/"+project+"/"+pod):
                        os.makedirs(outdirmeta+"/"+project+"/"+pod)
                    print pod
                    print indir+"/"+project+"/"+pod
                    po = polib.pofile(indir+"/"+project+"/"+pod)
                    pattern = re.compile('[^a-zA-Z0-9 ]+')
                    for entry in po.translated_entries():
                        tot += 1
                        # entry.msgid, entry.msgstr
                        sanitised = pattern.sub(' ', entry.msgstr)
                        words=pattern.sub('', sanitised).split(" ")
        
                        key = ",".join(map(lambda x:",".join(x), entry.occurrences))
        
                        if pod == "en_GB.po":
                            id_database[key] = [index, entry.msgid]
        
                        for word in words:
                            if len(word)>1:
                                wlower = word.lower()
                                pair = wlower[0:2]
                                
                                if not windex[pod].has_key(wlower[0:2]):
                                    windex[pod][wlower[0:2]] = {wlower:{project:[]}}
                                else:
                                    if not windex[pod][wlower[0:2]].has_key(wlower):
                                        windex[pod][wlower[0:2]][wlower] = {project:[]}
                                try:
                                    windex[pod][wlower[0:2]][wlower][project].append(id_database[key][0])
                                except KeyError:
                                    continue
        
                        try:
                            ourindex = str(id_database[key][0])
                            indexmeta[pod][int(ourindex)] = entry.msgstr
                        except KeyError:
                            continue
        
                        index += 1
        
            for pod in indexmeta:
                for p in range(0, len(indexmeta[pod]), index_lim):
                    f = open(outdirmeta+"/"+project+"/"+pod+"/"+str(p),"w")
                    todump = {}
                    for a in range(p, p+index_lim):
                        try:
                            todump[a] = indexmeta[pod][a]
                        except KeyError:
                            if p<len(indexmeta[pod]):
                                continue
                            else:
                                break
                    json.dump(todump, f)
                    f.close()
        
            for pod in windex:
                for pair in windex[pod]:
                    odir = outdir+"/"+pod+"/"+pair
                    if not os.path.exists(odir):
                        os.makedirs(odir)
        
                    if os.path.exists(outdir+"/"+pod+"/"+pair+"/"+pair):
                        f = open(outdir+"/"+pod+"/"+pair+"/"+pair)
                        old_windex = json.load(f)
                        f.close()
        
                        for word in windex[pod][pair]:
                            if old_windex.has_key(word):
                                old_windex[word][project] = windex[pod][pair][word][project]
                            else:
                                old_windex[word] = windex[pod][pair][word]
                        
                        f = open(outdir+"/"+pod+"/"+pair+"/"+pair, "w")
                        json.dump(old_windex, f)
                        f.close()
                    else:
                        f = open(odir+"/"+pair, "w")
                        json.dump(windex[pod][pair], f)
                        f.close()
