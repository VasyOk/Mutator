# -*- coding: utf-8 -*-
import os
from urlparse import urlparse
import json
import itertools
from dakota import allInteger
from dakota import populate_data
from modify_url import parse_qs_m
from itertools import chain, combinations

exclusion = ['htm','html','mp4','jpeg','jpg','png','gif','mp3','svg','js','css','woff']

def json_load_byteified(file_handle):
    return _byteify(
        json.load(file_handle, object_hook=_byteify),
        ignore_dicts=True
    )

def json_loads_byteified(json_text):
    return _byteify(
        json.loads(json_text, object_hook=_byteify),
        ignore_dicts=True
    )

def _byteify(data, ignore_dicts = False):

    if isinstance(data, unicode):
        return data.encode('utf-8')

    if isinstance(data, list):
        return [ _byteify(item, ignore_dicts=True) for item in data ]

    if isinstance(data, dict) and not ignore_dicts:

        return {
            _byteify(key, ignore_dicts=True): _byteify(value, ignore_dicts=True)
            for key, value in data.iteritems()
        }

    return data

class Eva(object):

    def __init__(self,url,postbody,filename):
        global test
        self.url = url
        self.filename = filename
        if postbody:
            self.postbody = postbody
        else:
            self.postbody = ' '
        self._dict = allInteger(filename)

    def startMu(self):
        chain_subset = self.allIn()
        tigerSkull = self.createMutRequests(self.url,self.postbody,chain_subset)
        return tigerSkull

    def createUrl(self,str,pathmut,querymut,out):
        if pathmut:
            str += '/'+pathmut
        else:
            if out.path:
                str += out.path
        if querymut:
            str += '?'+querymut
        else:
            if out.query:
                str += '?'+out.query
        if out.params:
            str += ';'+out.params
        if out.fragment:
            str += '#'+out.fragment

        return str

    def createMutRequests(self,url,postbody,chain_subset):
        #store Mutated URLs
        tigerSkull = []
        if url:
            out = urlparse(url)

        for subset in chain_subset:
            str = ''
            if out.scheme:
                str+=out.scheme+'://'
            if out.netloc:
                str+=out.netloc
            pathmut,pathChangeFlag =self.intereptPath(out.path,subset)
            querymut,queryChangeFlag = self.intereptQuery(out.query,subset)
            postmut,postChangeFlag = self.intereptPost(self.postbody,subset)

            if pathChangeFlag == 0 and queryChangeFlag==0 and postChangeFlag==0:
                muUrl = ''
                muPost = ''
            elif pathChangeFlag == 1 and queryChangeFlag==0 and postChangeFlag ==0:
                muUrl = self.createUrl(str,pathmut,'',out)
                muPost = postbody
            elif pathChangeFlag == 0 and queryChangeFlag == 1 and postChangeFlag == 0:
                muUrl = self.createUrl(str,'',querymut,out)
                muPost = postbody
            elif pathChangeFlag == 0 and queryChangeFlag == 0 and postChangeFlag == 1:
                muUrl = self.createUrl(str,'','',out)
                muPost = postmut
            elif pathChangeFlag == 1 and queryChangeFlag == 1 and postChangeFlag == 0:
                muUrl = self.createUrl(str,pathmut,querymut,out)
                muPost = postbody
            elif pathChangeFlag == 1 and queryChangeFlag == 0 and postChangeFlag == 1:
                muUrl = self.createUrl(str,pathmut,'',out)
                muPost = postmut
            elif pathChangeFlag == 0 and queryChangeFlag == 1 and postChangeFlag == 1:
                muUrl = self.createUrl(str,'',querymut,out)
                muPost = postmut
            elif pathChangeFlag == 1 and queryChangeFlag == 1 and postChangeFlag == 1:
                muUrl = self.createUrl(str,pathmut,querymut,out)
                muPost = postmut
            if muPost and muUrl:
                tigerSkull.append((muUrl,muPost))
        return tigerSkull

    def allIn(self):
        urlCount,urlList,pCount,pList = self.colistAll(self.url,self.postbody)

        if not urlList and not pList:
            mutList = []
        elif urlList and not pList:
            mutList = urlList
        elif not urlList and pList:
            mutList = pList
        else:
            mutList = urlList+pList
        chain_subset = self.all_subsets(mutList)
        return chain_subset

    def colistAll(self,url,postbody):
        count = 0
        _allstore=[]
        if url:
            out = urlparse(url)

        if out.path:
            pathcount,pathList = self.getPath(out.path)
        else:
            pathcount = 0
            pathList = []
        
        if out.query:
            qCount,qList = self.getQuery(out.query)
        else:
            qCount = 0
            qList = []
        
        if postbody:
            pCount,pList = self.getPost(postbody)
        else:
            pCount=0
            pList=[]

        count = pathcount+qCount
        _allstore = pathList+qList

        return count,_allstore,pCount,pList

    def combinationFromList(self,_liveList):
        #for getting all the possible combination of
        for L in range(0, len(_liveList)+1):
            for subset in itertools.combinations(_liveList, L):
                print subset

    def all_subsets(self,_liveList):
        return chain(*map(lambda x: combinations(_liveList, x), range(0, len(_liveList)+1)))

    def checkAny(self,mList,iList):
        return not set(mList).isdisjoint(iList)

    def is_json(self,myjson):

      try:
        json_object = json.loads(myjson)
      except ValueError, e:
        return False
      return True

    def getPath(self,path):
        count = 0
        _partstore = []
        #if url is not a get request to a file
        if not os.path.splitext(path)[1]:
            #splitting up parts by backslash
            parts = [p1 for p1 in path.split('/') if p1]
            #enumerate through the splitted url path
            for pos,val in enumerate(parts):
                #if value in the splitted list is there in dictionary values which can be used for mutating
                #increment the counter of mutable parameter and store it in a list
                if val in self._dict:
                    count += 1
                    _partstore.append(val)

        return count,_partstore

    def getQuery(self,query):
        count = 0
        _partstore = []

        #if not query return count as zero and empty list
        if not query:
            return count,_partstore
        else:
            #parse the query - will return one dictionary
            _parts = parse_qs_m(query)

        #if there are not parts in query - return count as zero and empty list
        if not _parts:
            return count,_partstore
        else:
            #enumerate through keys in that dictionary
            for key in _parts:
                #if key is present in the mutable values list
                #increment the counter and store it to a list
                if key in self._dict:
                    count +=1
                    _partstore.append(key)

        return count,_partstore

    def getOpJson(self,mjson):
        count = 0
        _partstore =[]
        #check whether request is json
        if self.is_json(mjson):
            #bytify the dictionary
            _parts = json_loads_byteified(mjson)
            #check whether Bytified _parts is dictionary
            if isinstance(_parts,dict):
                #extract key value from the dictionary of post request body
                for key,value in _parts.iteritems():
                    #if key is there in mutable values - check the type of value and do appropriate solution
                    #if found anything increment the count and add the parameters
                    if key in self._dict:
                        if isinstance(value,list):
                            count+=1
                            _partstore.append(key)
                        elif isinstance(value,dict):
                            pass
                        else:
                            count+=1
                            _partstore.append(key)
                    elif isinstance(value,dict):
                        for k,v in value.iteritems():
                            if k in self._dict:
                                if isinstance(value,list):
                                    count+=1
                                    _partstore.append(key)
                                elif isinstance(value,dict):
                                    pass
                                else:
                                    count+=1
                                    _partstore.append(key)
        return count,_partstore

    def getPost(self,postbody):
        count = 0
        _partstore=[]
        #if post request body is null it will return count as zero and empty list
        if not postbody:
            return count,_partstore
        else:
            if self.is_json(postbody):
                count,_partstore = self.getOpJson(postbody)
            else:
                try:
                    count,_partstore = self.getQuery(postbody)
                except Exception:
                    return count,_partstore

        return count,_partstore

                    # if key in self._dict:

    def getValueFromDictionary(self,key):
        #return values in dictionary for mutation
        return self._dict[key]

    def intereptPath(self,path,mutList):
        if not mutList:
            return path,0
        #to store Mutated Path
        mutatedPath = ''
        #if url is not a get request to a file
        if not os.path.splitext(path)[1]:
            #splitting up parts by backslash
            parts = [p1 for p1 in path.split('/') if p1]
            #check if any of the parts are there in mutList
            if not self.checkAny(parts,mutList):
                return path,0
            #enumerate through the splitted url path
            for pos,val in enumerate(parts):
                if val.isdigit():
                    if parts[pos-1] in mutList:
                        changeList = self.getValueFromDictionary(parts[pos-1])
                        if len(changeList) == 1:
                            parts[pos]=changeList[0]
                        elif len(changeList) > 1:
                            parts[pos]=changeList[0]

            mutatedPath = "/".join(parts)

            return mutatedPath,1
        else:
            return path,0

    def intereptQuery(self,query,mutList):
        #return the query if mutList is empty
        if not mutList:
            return query,0
        #mutated Query for return
        mutatedQuery = ''
        #changeList - to store Values from Dictionary
        changeList = []
        #if not query return count as zero and empty list
        if not query:
            return '',0
        else:
            #parse the query - will return one dictionary
            _parts = parse_qs_m(query)

        if not _parts:
            return query,0
        else:
            #list of Keys From Query
            _dList = _parts.keys()
            #check whether any key in parts is present in mutList
            if not self.checkAny(_dList,mutList):
                return query,0
            #enumerate through keys in that dictionary
            for key in _parts:
                if key in mutList:
                    changeList = self.getValueFromDictionary(key)
                    if len(changeList) == 1:
                        _parts[key]=changeList[0]
                    elif len(changeList) > 1:
                        _parts[key] = changeList[0]

            i = 1
            for k,v in _parts.iteritems():
                if i==1:
                    i+=1
                    mutatedQuery = k + '=' +v
                else:
                    mutatedQuery+= '&'+ k + '=' +v

            return mutatedQuery,1

    def intereptDictionary(self,_parts,changeList,mutList,key,value):
        #flag - if change
        flag = -1

        if isinstance(value,int):
            _parts[key]=int(changeList[0])
        elif isinstance(value,dict):
            innerdict = value.copy()
            for k,v in innerdict.iteritems():
                if k in mutList:
                    c = self.getValueFromDictionary(k)
                    if len(c) == 1:
                        if isinstance(v,int):
                            flag = 1
                            innerdict[k]=int(c[0])
                        else:
                            flag = 1
                            innerdict[k]=c[0]
                    elif len(c) > 1:
                        if isinstance(v,int):
                            flag = 1
                            innerdict[k]=int(c[0])
                        else:
                            flag = 1
                            innerdict[k]=c[0]
            if flag == 1:
                _parts[key]= innerdict.copy()
                flag = -1
        elif isinstance(value,list):
            if isinstance(changeList[0],list):
                _parts[key] = changeList[0]
            else:
                _parts[key] = changeList[0]
        else:
            _parts[key] = changeList[0]

        return _parts

    def intereptJson(self,postbody,mutList):
        changeList = []
        _parts = json_loads_byteified(postbody)
        # print _parts
        if not _parts:
            return postbody,0
        else:
            if isinstance(_parts,dict):
                print _parts
                #list of Keys From PostBody
                _dList = _parts.keys()
                #check whether any key in parts is present in mutList
                if not self.checkAny(_dList,mutList):
                    return postbody,0
                for key,value in _parts.iteritems():
                    if key in mutList:
                        changeList = self.getValueFromDictionary(key)
                        if len(changeList) == 1:
                            _parts = self.intereptDictionary(_parts,changeList,mutList,key,value).copy()
                        elif len(changeList) > 1:
                            _parts = self.intereptDictionary(_parts,changeList,mutList,key,value).copy()
                _parts = json.dumps(_parts)
                return _parts,1

            else:
                return postbody,0

    def intereptPost(self,postbody,mutList):
        if not mutList:
            return postbody,0

        if not postbody:
            return ''
        else:
            if self.is_json(postbody):
                _parts,flag = self.intereptJson(postbody,mutList)
                if flag == 1:
                    return _parts,1
                elif flag == 0:
                    return postbody,0
                else:
                    return postbody,0
            else:
                _parts,flag = self.intereptQuery(postbody,mutList)
                if flag == 1:
                    return _parts,1
                elif flag == 0:
                    return postbody,0
                else:
                    return postbody,0




url = 'http://bjn.com/seamapi/v1/user/612747/live_meetings/6028893961/pairing_code/PSTN?role=USER&user_access_token=b20397bd310146f68ff2a3f8a12a588e&access_token=25d45e941c8a4fe999f3e45353ab9c8e@z1'
postre='{"endpointType":"PSTN","endpointName":"sas &amp;amp;lt;sas","userId":571932,"languageCode":"en","capabilities":["AUDIO"]}'

url ='https://bluejeans.com/z1/evt/user/237623723/v1/398/r60n8cbi/xhr_send'
postre = 'role=USER&user_access_token=b20397bd310146f68ff2a3f8a12a588e&access_token=25d45e941c8a4fe999f3e45353ab9c8e@z1'

url = 'https://bluejeans.com/seamapi/v1/enterprise/14404/attributes/6727?access_token=106703e2596748fbaf949ad112b7cccd'
postre = '{"name":"default_audio_connection","value":"ask","type":"ATTRIBUTE","id":6727,"enterprise_id":14404}'

url = 'https://bluejeans.com/scheduling/confirm_delee/4324793/ '
postre = '{"name":"default_audio_connection","value":"ask","type":"ATTRIBUTE","id":6727,"enterprise_id":14404}'
# obj = Eva(url,postre)
# print obj.allIn()
# obj.combinationFromList(['v1', 'user', 'live_meetings'])
# count,allList,pCount,pList =obj.colistAll(url,postre)
# aList = allList+pList
# print obj.intereptPath('/seamapi/v1/user/612747/live_meetings/6028893961/pairing_code/PSTN',('user','live_meetings',))
# print obj._dict
# print obj.intereptQuery('role=USER&user_access_token=b20397bd310146f68ff2a3f8a12a588e&access_token=25d45e941c8a4fe999f3e45353ab9c8e@z1',('userId',))
# obj.intereptPost('{"endpointType":"PSTN","endpointName":"sas &amp;amp;lt;sas","userId":571932,"languageCode":"en","capabilities":["AUDIO"]}',('userId','live_meetings',))
# print obj.intereptPost('{"endpointType":"PSTN","endpointName":"sas &amp;amp;lt;sas","userId":571932,"languageCode":"en","capabilities":["AUDIO"]}',('userId',))
# print obj._dict.keys()
# print obj.is_json(postre)
# g = obj.startMu()
# for i in range(0,len(g)):
#     print g[i][0]
#     print g[i][1]
