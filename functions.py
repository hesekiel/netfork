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

import socket
import modules.nf_exceptions as nfex


def open_connection(host, port, proto):

    if proto == 'tcp':
        s = socket.socket(type=socket.SOCK_STREAM)
    elif proto == 'udp':
        s = socket.socket(type=socket.SOCK_DGRAM)
    else:
        raise nfex.UnknownProtocolException("%s is not valid protocol name." % proto)

    s.setblocking(True)
    s.settimeout(5)
    s.connect((host, port))

    return s


def close_connection(s):
    s.close()
    return 0


def send_data(s, data):

    s.send(bytes(data, 'utf-8'))

    return 0


def send_recv_data(s, data):

    s.send(bytes(data, 'utf-8'))
    response = s.recv(1024)

    return response


def log():
    return 0
