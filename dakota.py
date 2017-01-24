from selena import Gomes
from urlparse import urlparse
import json
_c = ['user','userid','leaderid','leader_id','user_id','username']
data = {}

def populate_data(filename):
    with open(filename) as js:
        try:
            data = json.load(js)
        except ValueError:
            with open(filename,'w') as outt:
                json.dump({},outt)


def f2(seq):
   # order preserving
   checked = []
   for e in seq:
       if e not in checked:
           checked.append(e)
   return checked

def _byteify(data, ignore_dicts = False):
    # if this is a unicode string, return its string representation
    if isinstance(data, unicode):
        return data.encode('utf-8')
    # if this is a list of values, return list of byteified values
    if isinstance(data, list):
        return [ _byteify(item, ignore_dicts=True) for item in data ]
    # if this is a dictionary, return dictionary of byteified keys and values
    # but only if we haven't already byteified it
    if isinstance(data, dict) and not ignore_dicts:
        return {
            _byteify(key, ignore_dicts=True): _byteify(value, ignore_dicts=True)
            for key, value in data.iteritems()
        }
    # if it's anything else, return it in its original form
    return data

def reconstruct(data):
    newdict = {}
    for key in data:
        if len(data[key]) > 1:
            for val in data[key]:
                newdict.setdefault(key, []).append(str(val))
        elif len(data[key]) == 1:
            # newdict.setdefault(key,[]).append(_byteify(data[key][0]))
            newdict.setdefault(key,[]).append(str(data[key][0]))
            # newdict[key] =_byteify(data[key][0])
        # else:
        #     newdict.setdefault(key,[]).append(str(data[key]))
    return newdict

# print reconstruct(data)

def p():

    obj = Gomes()
# print obj.checkCount(reconstruct(data))
#     print reconstruct(data)
    _bootstrapped = obj.creatSingle(reconstruct(data))
    return _bootstrapped

def allInteger(filename=None):
    if filename is not None:
        with open(filename) as js:
            try:
                data = json.load(js)
            except ValueError:
                with open(filename,'w') as outt:
                    json.dump({},outt)
    
    obj = Gomes()
    _bootstrapped = obj.createMutableDataInteger(reconstruct(data))
    return _bootstrapped

def separateuser():
    _dict = p()
    _newdict = []
    nam = ''
    for name in _dict:
        if str(name).lower() in _c:
            _newdict.append(_dict[name][0])

    if len(set(_newdict)) == 1:
        nam = _newdict[0]
    else:
        nam = _newdict[0]

    with open(str(nam)+'.json','w') as outfile:
        json.dump(_dict,outfile)

def sepUser():

    with open('result.json') as js:
        try:
            resultData = json.load(js)
        except ValueError:
            with open('result.json','w') as outt:
                json.dump({},outt)

    obj = Gomes()
    _dict = obj.createMutableDataInteger(reconstruct(resultData))
    _newdict = []
    nam = ''
    for name in _dict:
        if str(name).lower() in _c:
            _newdict.append(_dict[name][0])

    if len(set(_newdict)) == 1:
        nam = _newdict[0]
    else:
        nam = _newdict[0]

    with open(str(nam)+'.json','w') as outfile:
        json.dump(_dict,outfile)

    return True
    
url = ''

# print reconstruct(data)
#print allInteger()
# print p()
# _dict = p()
# print _dict['live_meetings'][0]
