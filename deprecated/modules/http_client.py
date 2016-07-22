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


from functions import *

headers = ['Accept',
   'Accept-Charset',
   'Accept-Encoding',
   'Accept-Language',
   'Accept-Datetime',
   'Authorization',
   'Cache-Control',
   'Connection',
   'Cookie',
   'Content-Length',
   'Content-Encoding',
   'Content-transfer-encoding',
   'Content-MD5',
   'Content-type',
   'Date',
   'Expect',
   'From',
   'Host',
   'If-Match',
   'If-Modified-Since',
   'If-None-Match',
   'If-Range',
   'If-Unmodified-Since',
   'Max-Forwards',
   'Origin',
   'Pragma',
   'Proxy-Authorization',
   'Range',
   'Referer',
   'TE',
   'Transfer-Encoding',
   'Upgrade',
   'User-Agent',
   'Via',
   'Warning',
   'X-Requested-With',
   'DNT',
   'X-Forwarded-For',
   'X-Forwarded-Proto',
   'Front-End-Https',
   'X-ATT-DeviceIde',
   'X-Wap-Profile',
   'Proxy-Connection']

response_headers = [
'Access-Control-Allow-Origin',
'Accept-Ranges',
'Age',
'Allow',
'Cache-Control',
'Connection',
'Content-Encoding',
'Content-Language',
'Content-Length',
'Content-Location',
'Content-MD5',
'Content-Disposition',
'Content-Range',
'Content-Type',
'Date',
'ETag',
'Expires',
'Last-Modified',
'Link',
'Location',
'P3P',
'Pragma',
'Proxy-Authenticate',
'Refresh',
'Retry-After',
'Server',
'Set-Cookie',
'Status',
'Strict-Transport-Security',
'Trailer',
'Transfer-Encoding',
'Vary',
'Via',
'Warning',
'WWW-Authenticate',
'X-Frame-Options',
'X-XSS-Protection',
'X-WebKit-CSP',
'X-Content-Type-Options',
'X-Powered-By',
'X-UA-Compatible'
]

headers_type_one = [
'Accept'
'Accept-Charset',
'Accept-Language',
'Cache-Control',
'Connection',
'Content-Type'
'Expect',
'Pragma',
'Proxy-Connection'
]

headers_type_two = [
'Accept-Encoding',
'TE',
'Transfer-Encoding',
'X-Forwarder-For'
]

headers_type_three = [
'Content-Length',
'Max-Forwards',
'DNT'
]

http_requests = ['GET', 
        'POST', 
        'OPTIONS', 
        'HEAD', 
        'PUT', 
        'DELETE', 
        'TRACE', 
        'CONNECT',
        'PROPFIND',
        'PROPPATCH',
        'MKCOL',
        'COPY',
        'MOVE',
        'LOCK',
        'UNLOCK',
        'VERSION-CONTROL',
        'REPORT',
        'CHECKOUT',
        'UNCHECKOUT',
        'MKWORKSPACE',
        'UPDATE',
        'LABEL',
        'MERGE',
        'BASELINE-CONTROL',
        'MKACTIVITY',
        'ORDERPATCH',
        'ACL',
        'PATCH',
        'SEARCH']

counts = [0, 1, 5, 17, 33, 65, 129, 257, 513, 1025, 2049, 4097, 8193, 12288]
login = "root@root.com"
password = "toor"

strings = open("fuzzstrings/fuzzdb","r")
numbers = open("fuzzstrings/numberMutators","r")
delimiters = open("fuzzstrings/delimiters","r")

def httpfuzz_client(host, port, fuzztype):
	if fuzztype == "response":
	    while True:
	       	send_http_request(host, port, "GET /index.html HTTP/1.1\r\nHost: www.machine.com\r\nAccept-Encoding: gzip, x-gzip, compress, x-compress, deflate, identity, exi, pack200-gzip, SDCH, bzip2, peerdist\r\n\r\n")

	elif fuzztype == "request":
	    
	    #----------------------------------------------------------------------------------------------------------

	    print  "Sending http requests with response headers"
	    
	    for request in http_requests:
	        for header in response_headers:
	            print "Fuzzing " + request + " with " + header
	            send_http_request(host, port, request + " /index.html HTTP/1.1\r\nHost: www.machine.com\r\n" + header + ": random\r\n\r\n")
	    
	    #----------------------------------------------------------------------------------------------------------

	    print "MUTATION STAGE"

	    # In this stage the inputs are taken from external file and mutated with mutation functions
	    # implemented in functions.py. There are mutators for both alphanumeric and non alphanumeric characters.
	    # File can be easily overwritten, requests are taken from various sources.

	    file = open("httprequests.txt","r")
	    
	    for line in file:
	        print line
	        mutator_char(host, port, "GET /index.html HTTP/1.1\r\nHost: www.machine.com\r\n", line.strip("\r\n") + "\r\n\r\n", "http")
	        mutator_delimiter(host, port, "GET /index.html HTTP/1.1\r\nHost: www.machine.com\r\n", line.strip("\r\n") + "\r\n\r\n", "http")
	        strings.seek(0)
	        for number in numbers:
	            send_http_request(host, port, mutator_number(line,number))
	    
	    #----------------------------------------------------------------------------------------------------------

	    print "GENERATION STAGE"

	    # In this stage invalid requests are generated from the database of valid commands and headers.
	    # The exact methods used are mentioned right above the code. 


	    # All headers are concatenated and sent to target with various http commands

	    print "all headers at once..."
	    data = ""
	    for header in headers:
	        data = data + header + ": random\r\n"
	    for request in http_requests:
	        send_http_request(host, port, request + " /index.html HTTP/1.1\r\nHost: www.machine.com\r\n" + data + "\r\n")

	    #----------------------------------------------------------------------------------------------------------
	    
	    # All commands are concatenated and sent to target. 

	    print "all commands at once..."
	    data = ""
	    for command in http_requests:
	        data = data + command
	    data = data + "/index.html HTTP/1.1\r\nHost: www.machine.com\r\n\r\n"
	    send_http_request(host, port, data)

	    #----------------------------------------------------------------------------------------------------------

	    # All commands are sent with the same argument

	    data = ""
	    for command in http_requests:
	        data = data + command + " /index.html HTTP/1.1\r\nHost: www.machine.com\r\n"
	    send_http_request(host, port, data + "\r\n")

	    #----------------------------------------------------------------------------------------------------------

	    # Fuzzing strings are used as commands

	    print "request command forging..."
	    
	    for line in counts:
	        send_http_request(host, port, line*'A' + " /index.html HTTP/1.1\r\nHost: www.machine.com\r\n\r\n")
	    strings.seek(0)
	    for line in strings:
	        for c in counts:
	            send_http_request(host, port, int(c)*line.strip("\r\n") + " /index.html HTTP/1.1\r\nHost: www.machine.com\r\n\r\n")

	    #----------------------------------------------------------------------------------------------------------

	    # HTTP version is fuzzed with both character strings and various numbers

	    print "HTTP version fuzzing..."
	    for request in http_requests:
	        for line in counts:
	            send_http_request(host, port, request + " /index.html " + line*'A' + "\r\n\r\n")
	        strings.seek(0)
	        for line in strings:
	            for c in counts:
	                send_http_request(host, port, request + " /index.html " + int(c)*line.strip("\r\n") + "\r\n\r\n")
	        numbers.seek(0)
	        for line in numbers:
	            send_http_request(host, port, request + " /index.html HTTP/" + line.strip("\r\n") + "\r\n\r\n")
	            send_http_request(host, port, request + " /index.html HTTP/" + line.strip("\r\n") + "." + line.strip("\r\n") + "\r\n\r\n")

	    #----------------------------------------------------------------------------------------------------------

	    # Name of requested source is fuzzed

	    print "requested page fuzzing..."
	    for request in http_requests:
	        for line in counts:
	            send_http_request(host, port, request + " " + line*'A' + " HTTP/1.1\r\nHost: www.machine.com\r\n\r\n")
	            send_http_request(host, port, request + " /" + line*'A' + " HTTP/1.1\r\nHost: www.machine.com\r\n\r\n")
	        strings.seek(0)
	        for line in strings:
	            for c in counts:
	                send_http_request(host, port, request + " " + int(c)*line.strip("\r\n") + " HTTP/1.1\r\nHost: www.machine.com\r\n\r\n")
	                send_http_request(host, port, request + " /" + int(c)*line.strip("\r\n") + " HTTP/1.1\r\nHost: www.machine.com\r\n\r\n")
	    
	    #----------------------------------------------------------------------------------------------------------
	    
	    # Same principle as commands fuzzing - fuzzing strings are used as request headers.

	    print "header forging..."
	    for request in http_requests:
	        for line in counts:
	            send_http_request(host, port, request + " /index.html HTTP/1.1\r\nHost: www.machine.com\r\n" + line*'A' + ": random\r\n\r\n")
	        strings.seek(0)
	        for line in strings:
	            for c in counts:
	                send_http_request(host, port, request + " /index.html HTTP/1.1\r\nHost: www.machine.com\r\n" + int(c)*line.strip("\r\n") + ": random\r\n\r\n")
	    
	    #----------------------------------------------------------------------------------------------------------
	    
	    # Long strings are used as header arguments

	    print "high count fuzzing..."
	    for request in http_requests:
	        for header in headers:
	            print "Fuzzing " + request + " with " + header
	            for c in counts:
	                send_http_request(host, port, request + " /index.html HTTP/1.1\r\nHost: www.machine.com\r\n" + header + ": " + c*'A' + "\r\n\r\n")

	    #----------------------------------------------------------------------------------------------------------
	    
	    # All parts of request are repeated various times

	    print "repeating fuzzing..."
	    for request in http_requests:
	        for header in headers:
	            print "Fuzzing " + request + " with " + header
	            for c in counts:
	                send_http_request(host, port, request + " /index.html HTTP/1.1\r\nHost: www.machine.com\r\n" + int(c)*header + ": random\r\n\r\n")
	                send_http_request(host, port, int(c)*(request + " /index.html HTTP/1.1\r\nHost: www.machine.com\r\n" + header + ": random\r\n\r\n"))

	    for request in http_requests:
	        for c in counts:
	            send_http_request(host, port, request + " /index.html " + int(c)*"HTTP/1.1" + "\r\n\r\n")
	            send_http_request(host, port, int(c)*request + " /index.html HTTP/1.1\r\nHost: www.machine.com\r\n\r\n")
	            send_http_request(host, port, request + int(c)*" /index.html " + "HTTP/1.1\r\nHost: www.machine.com\r\n\r\n")
	    
	    #----------------------------------------------------------------------------------------------------------
	    
	    # Fuzzing strings are used as header arguments

	    print "specific header arguments fuzzing..."

	    for request in http_requests:
	        
	        for header in headers:
	            print "Fuzzing " + request + " with " + header
	            for c in counts:
	                send_http_request(host, port, request + " /index.html HTTP/1.1\r\nHost: www.machine.com\r\n" + header + ": " + c*'A' + "\r\n\r\n")
	            strings.seek(0)
	            for line in strings:
	                send_http_request(host, port, str(request) + " /index.html HTTP/1.1\r\nHost: www.machine.com\r\n" + header + ": " + line.strip("\r\n") + "\r\n\r\n")
	            numbers.seek(0)
	            for line in numbers:
	                send_http_request(host, port, str(request) + " /index.html HTTP/1.1\r\nHost: www.machine.com\r\n" + header + ": " + line.strip("\r\n") + "\r\n\r\n")
	            delimiters.seek(0)
	            for line in delimiters:
	                for c in counts:
	                    send_http_request(host, port, str(request) + " /index.html HTTP/1.1\r\nHost: www.machine.com\r\n" + header + ": " + int(c)*line.strip("\r\n") + "\r\n\r\n")
	                    send_http_request(host, port, str(request) + " " + int(c)*line.strip("\r\n") + "index.html HTTP/1.1\r\nHost: www.machine.com\r\n" + header + int(c)*line.strip("\r\n") + " " + int(c)*line.strip("\r\n") + "\r\n\r\n")                
	        
	        for header in headers_type_one:
	            delimiters.seek(0)
	            for delimiter in delimiters:
	                send_http_request(host, port, str(request) + " /index.html HTTP/1.1\r\nHost: www.machine.com\r\n" + header + ": text" + delimiter + "plain\r\n\r\n")
	                for c in counts:
	                    send_http_request(host, port, str(request) + " /index.html HTTP/1.1\r\nHost: www.machine.com\r\n" + header + ": text" + int(c)*delimiter + "plain\r\n\r\n")
	            strings.seek(0)
	            for line in strings:
	                send_http_request(host, port, str(request) + " /index.html HTTP/1.1\r\nHost: www.machine.com\r\n" + header + ": text/" + line.strip("\r\n") + "\r\n\r\n")
	                send_http_request(host, port, str(request) + " /index.html HTTP/1.1\r\nHost: www.machine.com\r\n" + header + ": " + line.strip("\r\n") + "/plain\r\n\r\n")
	        
	        for header in headers_type_two:
	            for c in counts:
	                send_http_request(host, port, str(request) + " /index.html HTTP/1.1\r\nHost: www.machine.com\r\n" + header + ": text" + int(c)*(", text") + "\r\n\r\n")
	                send_http_request(host, port, str(request) + " /index.html HTTP/1.1\r\nHost: www.machine.com\r\n" + header + ": text" + int(c)*"," + "text\r\n\r\n")
	                delimiters.seek(0)
	                for delimiter in delimiters:
	                    send_http_request(host, port, str(request) + " /index.html HTTP/1.1\r\nHost: www.machine.com\r\n" + header + ": text" + int(c)*delimiter + "text\r\n\r\n")

	        for header in headers_type_three:
	            numbers.seek(0)
	            for number in numbers:
	                send_http_request(host, port, str(request) + " /index.html HTTP/1.1\r\nHost: www.machine.com\r\n" + header + ": " + number.strip("\r\n") + "\r\n\r\n")
	    
	    #----------------------------------------------------------------------------------------------------------    
