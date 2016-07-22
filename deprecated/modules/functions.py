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

import socket, time, re, string


login = "root@root.com"
password = "toor"
timeout = 0.1

fuzzes = open("fuzzstrings/fuzzdb", "r")

def send_http_request(host, port, text):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, int(port)))
        sock.send(text)
        time.sleep(timeout)
        sock.close()
    except KeyboardInterrupt:
        exit(0)

def send_imap_request_noauth(host, port, text):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, int(port)))
        sock.send(text)
        time.sleep(timeout)
        sock.close()
    except KeyboardInterrupt:
        exit(0)

def send_imap_request(host, port, login, password, command, firstarg, argcount=1, secondarg=""):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host,int(port)))
        sock.send("a login " + login + " " + password + "\r\n")
        sock.recv(4096)
        if argcount == 1:
            sock.send(command + " " + firstarg + "\r\n")
        elif argcount == 2:
            sock.send(command + " " + firstarg + " " + secondarg + "\r\n")
        time.sleep(timeout)
        sock.close()
    except KeyboardInterrupt:
        exit(0)

def send_imap_request_special(host, port, login, password, string):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host,int(port)))
        sock.send("a login " + login + " " + password + "\r\n")
        sock.recv(4096)
        sock.send(string)
        time.sleep(timeout)
        sock.close()
    except KeyboardInterrupt:
        exit(0)

def send_http_response(sock, data):
    print "Waiting for connection..."
    try:
        sock.listen(3)
        conn, addr = sock.accept()
        print "Connected (" + str(addr) + ")"
        conn.recv(4096)
        conn.send(data)
        conn.close()
    except KeyboardInterrupt:
        exit(0)


def send_imap_response(sock, command):
    try:
        print "Waiting for connection..."
        sock.listen(3)
        conn, addr = sock.accept()
        print "Connected (" + str(addr) + ")"
        conn.recv(4096)
        conn.send("* OK connected\r\n")
        conn.send(command)
        conn.close()
    except KeyboardInterrupt:
        exit(0)

def send_imap_response_noauth(sock, command):
    try:
        print "Waiting for connection..."
        sock.listen(3)
        conn, addr = sock.accept()
        print "Connected (" + str(addr) + ")"
        conn.recv(4096)
        conn.send(command)
        conn.close()
    except KeyboardInterrupt:
        exit(0)
        
# Mutator that finds every delimiter character in string and replace it with various count of other delimiters
counts = [0, 1, 5, 1025, 65, 129, 257, 1025, 2048, 4096, 12228, 65535]

def mutator_delimiter(host, port, unmutable, mutable, type, request=1, sock=None):
    delimiters = open("fuzzstrings/delimiters","r")
    i = 0
    for char in mutable:
        delimiters.seek(0)
        if char.isalpha() == False:
            temp = char
            for delimiter in delimiters:
                for c in counts:
                    fuzz = mutable[:i]
                    fuzz += int(c)*delimiter.strip("\r\n")
                    fuzz += mutable[i+1:]
                    if type == "http":
                        if request == 1:
                            send_http_request(host, port, unmutable + fuzz)
                        else:
                            send_http_response(sock, unmutable + fuzz)
                    elif type == "imap":
                        if request == 1:
                            send_imap_request_special(host, port, login, password, unmutable + fuzz)
                        else:
                            send_imap_response_noauth(sock, unmutable + fuzz)
        
        i += 1

# Mutator that finds every alphabetic character in string and repeats it/replaces it with various fuzzing strings 

def mutator_char(host, port, unmutable, mutable, type, request=1, sock=None):
    i = 0
    for char in mutable:
        if char.isalpha() == True:
            temp = char
            for c in counts:
                fuzz = mutable[:i]
                fuzz += int(c)*mutable[i]
                fuzz += mutable[i+1:]
                if type == "http":
                    if request == 1:
                        send_http_request(host, port, unmutable + fuzz)
                    else:
                        send_http_response(sock, unmutable + fuzz)
                elif type == "imap":
                    if request == 1:
                        send_imap_request_special(host, port, login, password, unmutable + fuzz)
                    else:
                        send_imap_response_noauth(sock, unmutable + fuzz)
            fuzzes.seek(0)
            for sym in fuzzes:
                for c in counts:
                    fuzz = mutable[:i]
                    fuzz += int(c)*sym
                    fuzz += mutable[i+1:]
                    if type == "http":
                        if request == 1:
                            send_http_request(host, port, unmutable + fuzz)
                        else:
                            send_http_response(sock, unmutable + fuzz)
                    elif type == "imap":
                        if request == 1:
                            send_imap_request_special(host, port, login, password, unmutable + fuzz)
                        else:
                            send_imap_response(sock, unmutable + fuzz)
        i += 1

# mutator that replaces every number of string with fuzzing string

def mutator_number(mutable, fuzz):
    return re.sub('[%s]' % string.digits, fuzz, mutable)