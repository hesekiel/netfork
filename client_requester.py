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

import optparse
from modules.http_client import *
from modules.imap_client import *


def sender(host, prot, fuzztype):

    if (prot == "HTTP") | (prot == "HTML"):
        port = 80
        httpfuzz_client(host, port, fuzztype)
    
    elif prot == "IMAP":
        port = 143
        imapfuzz_client(host, port, fuzztype)
            
parser = optparse.OptionParser("Usage: -H <target_host> -p <target_protocol> -t <request|response>\r\nAvailable protocols : HTTP | IMAP")
parser.add_option('-H', '--host', dest="host", type="string", default="192.168.56.1")
parser.add_option('-p', '--prot', dest="protocol", type="string", default="HTTP")
parser.add_option('-t', '--type', dest="type", type="string", default="response")

(options, args) = parser.parse_args()

host = options.host
prot = options.protocol
fuzztype = options.type

sender(host, prot, fuzztype)
