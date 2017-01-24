# -*- coding: utf-8 -*-
import urllib2
import requests
import httplib


def returnRequest(url,data,header):
    return urllib2.Request(url,data=data,headers=header)


def tigerInject(method,tigerSkull,header,ur,reqb):
    print '\033[1m==========ORIGINAL REQUEST==========\033[0m'
    print '\033[1mRequest:\033[0m {} {}'.format(method, ur)
    if method != 'GET':
        print '\033[1mPayload:\033[0m {}'.format(reqb)
    print '\r\n'

    for i in range(0,len(tigerSkull)):
        print "\033[4m\033[1mMutating Values: #{}\033[0m".format(i)
        print '\033[1mRequest:\033[0m {} {}'.format(method, tigerSkull[i][0])
        if method != 'GET':
            print '\033[1mPayload:\033[0m {}'.format(tigerSkull[i][1])

        try:
            if method == 'GET':
                url = tigerSkull[i][0]
                request = returnRequest(url,None,header)
                response = urllib2.urlopen(request,timeout=10)
                print '\033[1mResponse Code:\033[0m {}'.format(response.code)
                response.close()
            elif method == 'POST':
                url = tigerSkull[i][0]
                data = tigerSkull[i][1]
                print data
                data = data.replace('": ','":')
                data = data.replace(', ',',')
                request = returnRequest(url,data,header)
                response = urllib2.urlopen(request,timeout=10)
                print '\033[1mResponse Code:\033[0m {}'.format(response.code)
                response.close()
            elif method == 'PUT':
                url = tigerSkull[i][0]
                data = tigerSkull[i][1]
                data = data.replace('": ','":')
                data = data.replace(', ',',')
                request = returnRequest(url,data,header)
                request.get_method = lambda: 'PUT'
                response = urllib2.urlopen(request,timeout=10)
                print '\033[1mResponse Code:\033[0m {}'.format(response.code)
                response.close()
            elif method == 'DELETE':
                url = tigerSkull[i][0]
                request = returnRequest(url,None,header)
                request.get_method = lambda: 'DELETE'
                response = urllib2.urlopen(request,timeout=10)
                print '\033[1mResponse Code:\033[0m {}'.format(response.code)
                response.close()
        except urllib2.HTTPError, e:
            if e.code == 404:
                print '\033[1mError Code:\033[0m {}'.format(e.code)
                print '\033[1mError Message:\033[0m Page Not Found'
            elif e.code == 403:
                print '\033[1mError Code:\033[0m {}'.format(e.code)
                print '\033[1mError Message:\033[0m Access Denied'
            elif e.code == 401:
                print '\033[1mError Code:\033[0m {}'.format(e.code)
                print '\033[1mError Message:\033[0m UnAuthorized'
            elif e.code == 405:
                print '\033[1mError Code:\033[0m {}'.format(e.code)
                print '\033[1mError Message:\033[0m Method Not Allowed'
            else:
                print '\033[1mError Code:\033[0m {}'.format(e.code)
                print '\033[1mError Message:\033[0m Something Weird Happened'
        except urllib2.URLError, e:
            print '\033[1mError Code:\033[0m {}'.format(e.code)
            print '\033[1mError Message:\033[0m {}'.format(e.reason)
        except requests.exceptions.SSLError as e:
            print '\033[1mError Code:\033[0m {}'.format(e.code)
            print '\033[1mError Message:\033[0m {}'.format(e.reason)
        except httplib.HTTPException, e:
            print '\033[1mError Code:\033[0m {}'.format(e.code)
            print '\033[1mError Message:\033[0m {}'.format(e.reason)
        except Exception:
            print '\033[1mError Message:\033[0m Generic Exception'
        print "\r\n"
    

    print '\033[1m====================================\033[0m\r\n'