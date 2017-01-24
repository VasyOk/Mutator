#!/usr/bin/env python
# -*- coding: utf-8 -*-
#encoding=utf8
import sys,os,logging
reload(sys)
sys.setdefaultencoding('utf8')
from inject import tigerInject
from logical_proxy_input import Eva
from selena import Gomes
import json
from urlTec import URLExtractor
from urlparse import urlparse
import time
import socket
import re
import fcntl
import errno
from tld import get_tld
import os.path
logging.basicConfig(level=logging.DEBUG)
counter = 0
current_dir = os.path.dirname(os.path.abspath(__file__))
running_processes = {}
ip_re = re.compile(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")

from libmproxy import flow, proxy
from libmproxy.proxy.server import ProxyServer

class ProxyFlowMaster(flow.FlowMaster):

    def __init__(self, server, state, app_url, app_name, generate):
        flow.FlowMaster.__init__(self, server, state)

        self.generate = generate
        parsed_url = urlparse(app_url)
        netloc = parsed_url.netloc
        if not ip_re.match(netloc):
            self.netloc = get_tld(app_url)
        else:
            self.netloc = netloc

        self.filename = current_dir + '/dataset/' + app_name + '.json'
        if not os.path.isfile(self.filename):
            file_handle = open(self.filename, 'w')
            file_handle.write('{}')
            file_handle.close()

    def run(self):
        try:
            flow.FlowMaster.run(self)
        except KeyboardInterrupt:
            self.shutdown()

    def handle_request(self, f):
        request_flow = flow.FlowMaster.handle_request(self, f)
        if request_flow:
            request_flow.reply()

        header = request_flow.request.headers
        method = request_flow.request.method
        url = request_flow.request.url
        if request_flow.request.body:
            request_body = request_flow.request.body
        else:
            request_body = ' '

        parsed = urlparse(url)
        netloc = parsed.netloc
        if not ip_re.match(netloc):
            sub_loc = get_tld(url)
        else:
            sub_loc = netloc

        if sub_loc != self.netloc:
            pass
        else:
            if self.generate:
                print 'Starting Dataset Generation for URL: ' + str(url)
                obj = URLExtractor(url,request_body)
                pout,uout,reqout = obj.parseUrl()
                if not uout and not reqout:
                    pass
                else:
                    global counter
                    if not counter == 1000000000000:
                        counter += 1
                        stringdict = {}
                        with open(self.filename) as inp:
                            stringdict = json.load(inp).copy()
                            _eva = {}
                            selenobj = Gomes()
                            if not stringdict:
                                # print 'string empty'
                                _eva = {"host":"check"}.copy()
                            else:
                                _eva = stringdict.copy()

                            if not reqout and not uout:
                                pass
                            else:
                                with open(self.filename,'w') as outt:
                                    json.dump(selenobj.storetodict(uout,reqout,_eva),outt)

                            print counter
                    else:
                        selenobj = Gomes()
                        with open(self.filename) as inp:
                                # print 'one'
                            stringdict =json.load(inp).copy()

                        selenobj.checkCount(stringdict)
                        raise SystemExit
                        raise SystemExit

            else:
                print 'Starting Classification of URL: ' + str(url)
                obj = Eva(url,request_body,self.filename)
                tigerList = obj.startMu()
                if not tigerList:
                    pass
                else:
                    tigerInject(method,tigerList,header,url,request_body)
        return request_flow

    def handle_response(self, f):
        response_flow = flow.FlowMaster.handle_response(self, f)

        if response_flow:
            response_flow.reply()

        return response_flow

# Start Proxy on the specified Port
def start_proxy(app_url, app_name="test", port_no=2820, generate=True):
    config = proxy.ProxyConfig(
        port=port_no,
        # use ~/.mitmproxy/mitmproxy-ca.pem as default CA file.
        cadir=os.path.dirname(os.path.realpath(__file__))
    )

    state = flow.State()
    server = ProxyServer(config)

    flowMaster = ProxyFlowMaster(server, state, app_url, app_name, generate)
    print "Proxy Started on port " + str(port_no)
    flowMaster.run()

if __name__ == '__main__':
    lock_file = current_dir + '/proxy.lock'
    f = open(lock_file, 'w')
    try:
        fcntl.lockf(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except IOError, e:
        if e.errno == errno.EAGAIN:
            sys.stderr.write('Script already running')
            sys.exit(-1)
        raise

    app_url = 'https://cloudsek.com'
    app_name = 'cloudsek_app'
    port_no = 2820
    generate = True

    try:
       start_proxy(app_url, app_name, port_no, generate)
    except KeyboardInterrupt:
       print "Interrupt Received!"
       print "Bye..."
       sys.exit()
