# -*- coding: utf-8 -*-

import re
import json
from ast import literal_eval
import os
import operator
from urlparse import urlparse
from urlparse import parse_qs
from urlparse import parse_qsl
import pandas as pd
from modify_url import parse_qs_m
import numbers
from modify_url import unquote
exclusion = ['htm','html','mp4','jpeg','jpg','png','gif','mp3','svg','js','css','woff','json','swf']

class URLExtractor(object):
    '''
        URLExtractor Class contains all the functions for extracting information about a url

        Which initialize its object with an URL and a dictionary which contains label and corpus

        While creating object of URLExtractor pass the Incoming URL
    '''

    def __init__(self,url,reqbody=''):
        '''
        :param url: The Incoming URL to the object
        :param corpus: Initialize variable with Corpus
        :return:
        '''
        self.url = url
        self.corpus = self.readDatasettoDict()

        #print type(reqbody)
        if reqbody[0] is '[':
            reqbody = reqbody.replace('["[','[').replace(']"]',']')
            reqbody = reqbody.replace('\\"','"')
            self.reqbody = json.loads(reqbody)

        elif reqbody[0] is '{':
            reqbody = reqbody.replace('\\"','"').replace('{"{','{').replace('}"}','}')
            self.reqbody = json.loads(reqbody)
        elif self.is_json(reqbody):
            reqbody = unquote(reqbody)
            # self.reqbody = ast.literal_eval(reqbody)
            self.reqbody = json.loads(reqbody)
        else:
            reqbody = unquote(reqbody)
            self.reqbody = reqbody


    '''
        is_json function is to check whether the string passed is a dictionary or not
        if it is returns True otherwise returns False
    '''
    def is_json(self,myjson):

      try:
        json_object = json.loads(myjson)
      except ValueError, e:
        return False
      return True

    def isfloat(self,str):
        try:
            float(str)
        except ValueError:
            return False
        return True

    def readDatasettoDict(self):
        '''
        Read the Classification corpus and convert it into python dictionary
        :return: dictionary which contains Classification Corpus
        '''
        return pd.Series.from_csv('./dataset/corpus.csv', header=None).to_dict()

    def processnetloc(self):
        '''
        processnetloc extracts username, password, port from FTP protocols
        and hostname from both HTTP and FTP

        Whole information is stored in array named felice and returned
        :return:
        '''
        felice = []
        if not self.username():
            pass
        else:
            felice = operator.add(felice,[('Username',self.username())])
        if not self.password():
            pass
        else:
            felice = operator.add(felice,[('PASSWORD',self.password())])
        if not self.hostname():
            pass
        else:
            felice = operator.add(felice,[('HOSTNAME',self.hostname())])
        if not self.port():
            pass
        else:
            felice = operator.add(felice,[('PORT',self.port())])
        return felice


    def processqpf(self):
        '''
        This function will collect information from the query segment, path segment, fragment and parameter section in url
        and it is stored in an dictionary named url_data.

        after storing it in dictionary it will return it
        :return:
        '''
        url_data = {}

        if not self.processquery():
            pass
        else:
            for name, value in self.processquery():
                if name in url_data:
                    continue
                else:
                    url_data[name] = value
        if not self.processpath():
            pass
        else:
            for name, value in self.processpath():
                if name in url_data:
                    continue
                else:
                    url_data[name] = value
        if not self.processfragment():
            pass
        else:
            for name, value in self.processfragment():
                if name in url_data:
                    continue
                else:
                    url_data[name] = value
        if not self.processparams():
            pass
        else:
            for name, value in self.processparams():
                if name in url_data:
                    continue
                else:
                    url_data[name] = value

        return url_data

    def listop(self,reqbo):
        if isinstance(reqbo,dict):
            return reqbo
        else:
            return {}

    def processreqbody(self):
        '''
        Function to manage the POST Requests through the network

        If the post request is a json object or a dictionary this will check and return it

        if it is not a json object it will process it using parse_qs_m and return it
        :return:
        '''
        #print self.reqbody
        if isinstance(self.reqbody,dict):
            return self.reqbody
        elif isinstance(self.reqbody,list):
            if len(self.reqbody) > 1:
                z = {}
                for i in range(0,len(self.reqbody)):

                    incoming = self.listop(self.reqbody[i])
                    z.update(incoming.copy())
                return z
            elif len(self.reqbody) == 1:
                if isinstance(self.reqbody[0],dict):
                    return self.reqbody[0]
                elif len(self.reqbody[0])>1:
                    z = {}
                    for i in range(0,len(self.reqbody[0])):
                        incoming = self.listop(self.reqbody[0][i])
                        z.update(incoming.copy())
                    return z
                # return self.listop(self.reqbody)

            return {"None":"None"}
        else:
            return parse_qs_m(self.reqbody)

    def ticket(self,key,value,data_dict):
            '''
            Ticket is the function which does tagging
            We have to pass the dictionary to bind with previous data, the key and the value
            which returns dictionary with key, value and its tag
            in the form :- 'key' : [['value','tag']]
            :param key:
            :param value:
            :param data_dict:
            :return:
            '''
            if isinstance(value,dict):
                '''
                checking if a value is json object. if json object it will be passed through the function tagg
                and update the super dictionary data_dict
                '''
                temp_data_dict = data_dict.copy()
                temp_data_dict.update(self.tagg(value))
                data_dict.clear()
                data_dict = temp_data_dict.copy()
                del temp_data_dict
            elif isinstance(value,list):
                '''
                checking if value is a list of json objects,
                if so tagg the whole json objects in the list
                '''
                for i in range(0,len(value)):
                    if isinstance(value[i],dict):
                        temp_data_dict = data_dict.copy()
                        temp_data_dict.update(self.tagg(value[i]))
                        data_dict.clear()
                        data_dict = temp_data_dict.copy()
                        del temp_data_dict
                    else:
                        continue
            else:
                '''
                if it is normal value.
                tagg them based on values - if it is integer,alpha, hash tag them like that
                '''
                extractedvalue = str(value)

                if not self.corpus.has_key(key.lower()):
                    '''
                    This section will tagg if variable is not present in the dataset
                    '''
                    if extractedvalue.isdigit():
                        if not key in data_dict:
                            data_dict.setdefault(key, []).append([value,'INTEGER_OTHER'])
                    elif extractedvalue.isalpha():
                        if not key in data_dict:
                            data_dict.setdefault(key, []).append([value,'ALPHA_OTHER'])
                    elif extractedvalue.isalnum():
                        if not key in data_dict:
                            data_dict.setdefault(key, []).append([value,'HASH_OTHER'])
                    elif self.isfloat(extractedvalue):
                        if not key in data_dict:
                            data_dict.setdefault(key, []).append([value,'FLOAT_OTHER'])
                    elif self.is_json(extractedvalue):
                        extractedvalue = json.loads(extractedvalue)
                        temp_data_dict = data_dict.copy()
                        temp_data_dict.update(self.tagg(extractedvalue))
                        data_dict.clear()
                        data_dict = temp_data_dict.copy()
                        del temp_data_dict
                    else:
                        if not key in data_dict:
                            data_dict.setdefault(key, []).append([value,'OTHER'])
                else:
                    '''
                    This section will tagg if the variable is present in our dataset.
                    '''
                    if extractedvalue.isdigit():
                        if not key in data_dict:
                            data_dict.setdefault(key, []).append([value,'INTEGER_'+str(self.corpus.get(key.lower()))])
                    elif extractedvalue.isalpha():
                        if not key in data_dict:
                            data_dict.setdefault(key, []).append([value,'ALPHA_'+str(self.corpus.get(key.lower()))])
                    elif extractedvalue.isalnum():
                        if not key in data_dict:
                            data_dict.setdefault(key, []).append([value,'HASH_'+str(self.corpus.get(key.lower()))])
                    elif self.isfloat(extractedvalue):
                        if not key in data_dict:
                            data_dict.setdefault(key, []).append([value,'FLOAT_'+str(self.corpus.get(key.lower()))])
                    elif self.is_json(extractedvalue):

                        extractedvalue = json.loads(extractedvalue)
                        temp_data_dict = data_dict.copy()
                        temp_data_dict.update(self.tagg(extractedvalue))
                        data_dict.clear()
                        data_dict = temp_data_dict.copy()
                        del temp_data_dict
                    else:
                        if not key in data_dict:
                            data_dict.setdefault(key, []).append([value,self.corpus.get(key.lower())])
            return data_dict

    def checkVariable(self,key,reqbody):
        if key in str(reqbody):
            return True
        else:
            return False

    def tagg(self,url_data):
        '''
        Super Tagg function from here original tagging done
        check if variable is a SEO Parsed Variable then will discard that variable and value

        if value is some files in the server, exclude that also
        :param url_data:
        :return:
        '''

        data_dict = {}
        for key in url_data:

            if '-' in key or not len(key) < 60:
                checked = self.checkVariable(key,self.reqbody)
                if checked ==  True:
                    data_dict = self.ticket(key,url_data.get(key),data_dict)
                elif checked == False:
                    continue
                else:
                    continue

            elif os.path.splitext(str(url_data.get(key)))[1]:

                if not os.path.splitext(str(url_data.get(key)))[1].split('.')[1] in exclusion:

                    data_dict = self.ticket(key,str(url_data.get(key)),data_dict)
                    self.innerurl = urlparse(url_data.get(key))
                    if not self.innerurl.query:
                        continue
                    else:
                        for name,val in parse_qsl(self.innerurl.query):
                            data_dict = self.ticket(name,val,data_dict)
                    if not self.innerurl.path:
                        continue
                    else:
                        for name,val in parse_qsl(self.innerurl.path):
                            data_dict = self.ticket(name,val,data_dict)
                    if not self.innerurl.params:
                        continue
                    else:
                        for name,val in parse_qsl(self.innerurl.params):
                            data_dict = self.ticket(name,val,data_dict)
                    if not self.innerurl.fragment:
                        continue
                    else:
                        for name,val in parse_qsl(self.innerurl.fragment):
                            data_dict = self.ticket(name,val,data_dict)
                else:
                    continue
            else:
                data_dict = self.ticket(key,url_data.get(key),data_dict)

        return data_dict

    def parseUrl(self):
        '''

        :return: tagged output on the website location, GET Requests part and POST Requests
        '''
        self.out = urlparse(self.url)
        felice = self.processnetloc()
        url_data = self.processqpf()
        data_dict = self.tagg(url_data)
        michelle = self.tagg(self.processreqbody())

        return felice,data_dict,michelle

    def alphan(self,s):
        '''
        function to match alphanumeric tokens
        :param s: tokens
        :return: if match found returns true otherwise false
        '''
        return re.match(r'\w*\d+\w*',s)

    def processpath(self):
        '''
        function to process the path of URL and extract information from there
        :return: information include whether any extension files are there or identified alpha numberic ones
        '''
        path = self.out.path
        # exclusion = ['htm','html','mp4','jpeg','jpg','png','gif','mp3','svg','js','css','woff']
        if os.path.splitext(path)[1]:
            if not os.path.splitext(path)[1].split('.')[1] in exclusion:
                parts = [s1 for s1 in path.split('/') if s1]
                theta = [(parts[i-1],s1) for i,s1 in enumerate(parts) if os.path.splitext(s1)[1] if not os.path.splitext(s1)[1].split('.')[1].isdigit() if i != 0]
                alpha=[]
                for i,s1 in enumerate(parts):
                    if self.alphan(s1):
                        if i !=0:
                            alpha.append((parts[i-1],s1))
                        else:
                            alpha.append(('HOSTNAME',s1))
                if not theta and not alpha:
                    return None
                else:
                    return operator.add(theta,alpha)
            else:
                return None
        else:
            parts = [s1 for s1 in path.split('/') if s1]
            alpha=[]
            for i,s1 in enumerate(parts):
                if self.alphan(s1):
                    if i !=0:
                        alpha.append((parts[i-1],s1))
                    else:
                        alpha.append(('HOSTNAME',s1))
            if not alpha:
                return None
            else:
                return alpha

    def processquery(self):
        return parse_qsl(self.out.query)

    def processfragment(self):
        return parse_qsl(self.out.fragment)

    def processparams(self):
        return parse_qsl(self.out.params)

    def username(self):
        netloc = self.out.netloc
        if '@' in netloc:
            userinfo = netloc.rsplit('@', 1)[0]
            if ':' in userinfo:
                userinfo = userinfo.split(":", 1)[0]
            return userinfo
        return None

    def password(self):
        netloc = self.out.netloc
        if '@' in netloc:
            userinfo = netloc.rsplit('@', 1)[0]
            if ':' in userinfo:
                return userinfo.split(':', 1)[1]
        return None

    def hostname(self):
        netloc = self.out.netloc.split('@')[-1]
        if '[' in netloc and ']' in netloc:
            return netloc.split(']')[0][1:].lower()
        elif ':' in netloc:
            return netloc.split(':')[0].lower()
        elif netloc == '':
            return None
        else:
            return netloc.lower()

    def port(self):
        netloc = self.out.netloc.split('@')[-1].split(']')[-1]
        if ':' in netloc:
            port = netloc.split(':')[1]
            if port:
                port = int(port, 10)
                if (0 <= port <= 65535):
                    return port
        return None


def main():
    # url ='http://bjn-prod-django.s3.amazonaws.com/images/profile_pictures/peter.test6666_natalie.png?Signature=wP/gxjkYrjzVj0lJLw8OvB4farg=&Expires=1452610278&AWSAccessKeyId=AKIAIDM362L4ZM6M5UCA'
    # url = 'http://www.bluejeans.com:8080/seamapi/v1/user/612747/live_meetings/6028893961/pairing_code/SIP?role=USER&user_access_token=f5a4a74043e545a3bbe5abbf945a9854&access_token=e60c3de94f90443086e807cd02762f05%40z1'
    # url = 'ftp://ra@hul@57.23.56.14/'
    # url = 'https://www.linkedin.com/profile/view?id=AAIAAATrBqsBG60jpv36NHVOfvk-k0qT9Ab59TU&trk=nav_responsive_tab_profile'
    import time
    start_time = time.time()
    # url = 'http://bluejeans.com/isbn/1234567890/index'
    # url = 'https://mobapi.redbus.in/wdsvc/v1_1/seatlayout?rt=8533844&sourceId=122&destinationId=65791&doj=22-Jan-2016&ff={"grant_type":"a2m_user","userRole":"user","properties":{"userAccessToken":"1a927ff07a69467e931256d65713eebe","live_meetings":"6028893961"}}'
    s = '{"{"grant_type":"a2m_user","userRole":"user","properties":{"userAccessToken":"1a927ff07a69467e931256d65713eebe","live_meetings":"6028893961"}}"}'
    # s = 'hrllo'
    url = 'http://www.mycity4kids.com/booktickets/IdiomsThroughBasketrybyCraft-Village/58167/events/12'
    url = 'https://static.bluejeans.com/website/misc/jquery.once.js?v=1'
    url = 'https://www.bluejeans.com'
    # s = '%7B%22JourneyDetails%22%3A%7B%22CartInfo%22%3A%7B%7D%2C%22OnwardJourney%22%3A%7B%22RouteId%22%3A%228533844%22%2C%22DOJ%22%3A%2222-Jan-2016%22%2C%22Seats%22%3A%22S5%3A1%22%2C%22BordingPoint%22%3A%221229801%22%7D%7D%2C%22CustomerDetails%22%3A%7B%22PaxInfo%22%3A%5B%7B%22FirstName%22%3A%22adsasdfas%22%2C%22Title%22%3A%22Ms%22%2C%22Age%22%3A%2223%22%7D%5D%2C%22EmailId%22%3A%22reeeeeeeeeee%40gmail.com%22%2C%22Phone%22%3A%227898945789%22%2C%22AltPhone%22%3A%229889798999%22%2C%22Address%22%3A%22Maaaraaasdfa%22%2C%22ProofType%22%3A%22DrLicense%22%2C%22ProofNum%22%3A%2222%2F9856%2F2007%22%2C%22ProofPax%22%3A%22adsasdfas%22%7D%2C%22PaymentDetails%22%3A%7B%22PayMod%22%3A%22NETBANKING%22%2C%22PGInfo%22%3A%7B%22CardType%22%3A%22UTI_N%22%7D%2C%22IsJusPay%22%3Afalse%7D%2C%22AdditionalDetails%22%3A%7B%22ChTerms%22%3A%22on%22%2C%22OfferCode%22%3A%22%22%2C%22CouponCode%22%3A%22%22%2C%22CouponCodeValue%22%3A%22%22%2C%22RedirectionPageCount%22%3A0%2C%22Clip%22%3A%22122.166.239.166%22%2C%22IsPolicyRequired%22%3Afalse%2C%22PolicyFare%22%3A0%2C%22WalletUsed%22%3Afalse%2C%22Token%22%3A%22k1gfAIT28icCR4glLAvIiXDZtEO9rAn76001Dw3n98lxXQQnvWaNRtUmns8%252fPJAVJBcsF18GfecPkY57hU59iPNZ7hDWF___FROENemTRFHhLDeqCf22NY8c6KQhsz2ugdO3fAyGCE6Kwa4pSSy4U3JTfxnQ3ge8b1mCi4T1jzjXudnVx1ivlzQNhw7gf2___Z8akvt0Q7OjhF8%253d%22%7D%7D'
    # print (unquote(s))

    # print type(s)
    # url = 'https://web.whatsapp.com/img/30ac78e81e85b41455f2a256357c1139.svg'
    # s = unquote(s)
    # s = '["[\"meeting.register\",{\"numeric_id\":\"406969062\",\"access_token\":\"e096648d68524d1e91ea0ac32676862d@z1\",\"user\":{\"id\":863772,\"full_name\":\"Rahul R\",\"is_leader\":true},\"leader_id\":863772,\"protocol\":\"2\",\"events\":[\"meeting\",\"chat\",\"endpoint\",\"private_chat\"],\"chat_enabled\":true}]"]'
    # s = 'title=Cloudsek&start_timezone=Asia%2FKolkata&start_date=Wed%2C+Feb+17%2C+2016&start_time=100&start_am=0&end_date=Wed%2C+Feb+17%2C+2016&end_time=230&end_am=0&repeat_meeting=DAILY&repeat_meeting_frequency=1&repeat_meeting_sub_options_daily_weekdays=False&repeat_meeting_frequency_daily=1&repeat_meeting_week_of_month=0&repeat_meeting_day_of_month=17&repeat_meeting_day_of_week_monthly=1&recurssion_ending=NEVER&meeting_id_choice=dynamic&meeting_numeric_id=641433854&meeting_id=&guests=%3Cscript%3Ealert%28document.cookie%29%3C%2Fscript%3E%40mail.com&message=%3Cscript%3Ealert%28document.cookie%29%3C%2Fscript%3E&video_best_fit=on&is_moderator_less=on&disallow_chat=on'
    # s = '[{"name":"viewCount"}]'
    # s = ''
    # url = 'https://www.google.co.in/ads/user-lists/1015740975/?label=s0flCMG_3wMQr_Sr5AM&fmt=3&bg=ffffff&num=2&ct_cookie_present=false&cv=8&frm=0&url=https%3A//bluejeans.com/scheduling/%3Fsuccess%3Dtrue&ref=https%3A//bluejeans.com/iframe/login/%3Ffb%3Dtrue&random=793282569&ipr=y'
    url = 'https://www.titan.co.in/control/createNewCustomer'
    s = 'add_product_id=6111SL03&Titanprice=1795.00&quantity=1&clearSearch=N&priceRangeListing=price%3A%5B650+TO+4995%5D&maxPriceValue=148000.000&minPriceValue=399.000&SEARCH_STRING=Watches&searchParam=Watches&prevQuery=%7B!tag%3DbrandFQ%7Dbrand%3A(%22Fastrack%22)&pageName=catalogListing&catImageName=&pageBegin=3&optionVal=&pageCountNo=&add_amount='
    yulip = URLExtractor(url,s)

    print yulip.parseUrl()
    print time.time() - start_time

if __name__ == '__main__':
    main()
