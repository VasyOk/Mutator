from urlTec import URLExtractor

_abigail = {}

def f2(seq):
   # order preserving
   checked = []
   for e in seq:
       if e not in checked:
           checked.append(e)
   return checked

class Gomes(object):

    def __init__(self):
        pass

    def storetodict(self,info,reqinfo,_abigail):
        for key in info:
            value = info.get(key)[0][0]
            if not isinstance(info.get(key),dict):
                if key in _abigail:
                    _abigail[key].append(value)
                else:
                    _abigail[key] = [value]

        for key in reqinfo:
            value = reqinfo.get(key)[0][0]
            if not isinstance(reqinfo.get(key),dict):
                if key in _abigail:
                    _abigail[key].append(value)
                else:
                    _abigail[key] = [value]

        return _abigail

    def checkCount(self,_livedict):
        if not not _livedict:
            for key in _livedict:
                if len(_livedict[key]) > 1:
                    if len(_livedict[key]) > 1 and len(set(_livedict[key]))== 1:
                        print "These values are repeated without any change"
                        print key  + ' : ' +str(set(_livedict[key] ))
                    elif len(set(_livedict[key])) > 1:
                        print "different values repeated for the same variable"
                        print key + ' : ' + str(_livedict.get(key))
                else:
                    print 'Same Value'
                    continue

    def creatSingle(self,_livedict):
        _boostrapped = {}
        if not not _livedict:
            for key in _livedict:
                if len(_livedict[key]) > 1:
                    if len(_livedict[key]) > 1 and len(set(_livedict[key]))== 1:
                        # print "These values are repeated without any change"
                        _boostrapped[key] = f2(_livedict[key])
                        # print key  + ' : ' +str(set(_livedict[key] ))
                    elif len(set(_livedict[key])) > 1:
                        pass
                        # _boostrapped.setdefault(key, []).append(f2(_livedict[key]))
                        # print "different values repeated for the same variable"
                        # print key + ' : ' + str(_livedict.get(key))
                elif len(_livedict[key]) == 1:
                    _boostrapped[key] = _livedict[key]
                else:
                    # print 'Same Value'
                    continue
        return _boostrapped

    def createMutableDataInteger(self, _livedict):
        _bootstraped = {}
        if _livedict:
            for key in _livedict:
                value = _livedict[key]
                
                if len(value) == 1 and value[0].isdigit():
                    _bootstraped[key] = f2(value)
                elif len(f2(value)) == 1 and f2(value)[0].isdigit():
                    _bootstraped[key] = f2(value)
                elif len(f2(value)) > 1:
                    _store = []
                    for val in f2(value):
                        if val.isdigit():
                            _store.append(str(val))
                    if _store and len(_store) < 10:
                        _bootstraped[key] = f2(_store)
        
        if not _bootstraped:
            return {}
        else:
            return _bootstraped

def main():
    url = 'http://www.bluejeans.com:8080/seamapi/v1/user/612747/live_meetings/6028893961/pairing_code/SIP?role=USER&userRole=user&user_access_token=f5a4a74043e545a3bbe5abbf945a9854&access_token=e60c3de94f90443086e807cd02762f05%40z1'
    s = '{"grant_type":"a2m_user","userRole":"user","properties":{"userAccessToken":"1a927ff07a69467e931256d65713eebe"}}'
    # s ='%7B%22JourneyDetails%22%3A%7B%22CartInfo%22%3A%7B%7D%2C%22OnwardJourney%22%3A%7B%22RouteId%22%3A%228533844%22%2C%22DOJ%22%3A%2222-Jan-2016%22%2C%22Seats%22%3A%22S5%3A1%22%2C%22BordingPoint%22%3A%221229801%22%7D%7D%2C%22CustomerDetails%22%3A%7B%22PaxInfo%22%3A%5B%7B%22FirstName%22%3A%22adsasdfas%22%2C%22Title%22%3A%22Ms%22%2C%22Age%22%3A%2223%22%7D%5D%2C%22EmailId%22%3A%22reeeeeeeeeee%40gmail.com%22%2C%22Phone%22%3A%227898945789%22%2C%22AltPhone%22%3A%229889798999%22%2C%22Address%22%3A%22Maaaraaasdfa%22%2C%22ProofType%22%3A%22DrLicense%22%2C%22ProofNum%22%3A%2222%2F9856%2F2007%22%2C%22ProofPax%22%3A%22adsasdfas%22%7D%2C%22PaymentDetails%22%3A%7B%22PayMod%22%3A%22NETBANKING%22%2C%22PGInfo%22%3A%7B%22CardType%22%3A%22UTI_N%22%7D%2C%22IsJusPay%22%3Afalse%7D%2C%22AdditionalDetails%22%3A%7B%22ChTerms%22%3A%22on%22%2C%22OfferCode%22%3A%22%22%2C%22CouponCode%22%3A%22%22%2C%22CouponCodeValue%22%3A%22%22%2C%22RedirectionPageCount%22%3A0%2C%22Clip%22%3A%22122.166.239.166%22%2C%22IsPolicyRequired%22%3Afalse%2C%22PolicyFare%22%3A0%2C%22WalletUsed%22%3Afalse%2C%22Token%22%3A%22k1gfAIT28icCR4glLAvIiXDZtEO9rAn76001Dw3n98lxXQQnvWaNRtUmns8%252fPJAVJBcsF18GfecPkY57hU59iPNZ7hDWF___FROENemTRFHhLDeqCf22NY8c6KQhsz2ugdO3fAyGCE6Kwa4pSSy4U3JTfxnQ3ge8b1mCi4T1jzjXudnVx1ivlzQNhw7gf2___Z8akvt0Q7OjhF8%253d%22%7D%7D'
    yulip = URLExtractor(url,s)
    uinfo,reqinfo = yulip.parseUrl()
    oblu = Gomes()
    print oblu.storetodict(uinfo[1],reqinfo,_abigail)
    oblu.checkCount(oblu.storetodict(uinfo[1],reqinfo,_abigail))

if __name__ == '__main__':
    main()
