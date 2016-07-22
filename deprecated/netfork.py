#############################################################################################
# Copyright 2014 Ivo Nutar                                                                  #
#                                                                                           #
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file #
# except in compliance with the License.                                                    #
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0        #
#                                                                                           #
# Unless required by applicable law or agreed to in writing, software distributed under     #
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY   #
# KIND, either express or implied. See the License                                          #
# for the specific language governing permissions and limitations under the License.        #
#############################################################################################

# fuzzdb file under new BSD license
# fuzzdb (c) Copyright Adam Muntner, 2010, 2011

import socket
import signal
import sys
import time
from modules.http import *
from modules.imap import *
from modules.html import *
import optparse

class Server:

    imap_commands = [

    ]

    def __init__(self, prot, fuzztype):
        self.host = ''
        self.prot = prot
        self.fuzztype = fuzztype
        if(prot == "HTTP") | (prot == "HTML"):
            self.port = 80
        elif prot == "IMAP":
            self.port = 143
        else:
            print "Unknown protocol."
            sys.exit(1)

    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            print "Starting NetFork..."
            self.socket.bind((self.host, self.port))
        except Exception as e:
            print "Could not start NetFork (bad host or port):" + str(e) + "."
            sys.exit(1)
        print "NetFork running."
        self.listen(fuzztype)

    def listen(self, fuzztype):
        if fuzztype == "request":
            if prot == "HTTP":
                while True:
                    send_http_response(self.socket, "HTTP/1.1 200 OK\r\n\r\n")
            elif prot == "IMAP":
                while True:
                    send_imap_response(self.socket, "OK\r\n")
        else:
            if prot == "IMAP":
                imapfuzz(self.socket)
            elif prot == "HTTP":
                httpfuzz(self.socket)
            elif prot == "HTML":
                htmlfuzz(self.socket)

parser = optparse.OptionParser("Usage: netfork -H <target_host> -p <target_protocol>\r\nAvailable protocols : HTTP | IMAP")
parser.add_option('-H', '--host', dest="host", type="string", default="192.168.56.101")
parser.add_option('-p', '--prot', dest="protocol", type="string", default="HTTP")
parser.add_option('-t', '--type', dest="type", type="string", default="response")

(options, args) = parser.parse_args()

host = options.host
prot = options.protocol
fuzztype = options.type

print "Fuzzing protocol " + prot + " at host " + host + "\r\n"

if (host is None) | (prot is None) | (fuzztype is None):
    print parser.usage
    exit(0)

s = Server(prot, fuzztype)
s.start()
