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

import zlib
import socket
from functions import *

headers = [
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

headers_date = [
        'Date',
        'Expires',
        'Last-Modified',
        'Retry-After'
    ]

headers_address = [
        'Content-Location',
        'Location',
        'Refresh'
    ]

headers_number = [
        'Age',
        'Content-Length',
        'Retry-After',
    ]

response_codes = [
        '100 Continue',
        '101 Switching Protocols',
        '200 OK',
        '201 Created',
        '202 Accepted',
        '203 Non-Authoritative Information',
        '204 No Content',
        '205 Reset Content',
        '206 Partial Content',
        '300 Multiple Choices',
        '301 Moved Permanently',
        '302 Found',
        '303 See Other',
        '304 Not Modified',
        '305 Use Proxy',
        '306',
        '307 Temporary Redirect',
        '400 Bad Request',
        '401 Unauthorized',
        '402 Payment Required',
        '403 Forbidden',
        '404 Not Found',
        '405 Method Not Allowed',
        '406 Not Acceptable',
        '407 Proxy Authentication Required',
        '408 Request Timeout',
        '409 Conflict',
        '410 Gone',
        '411 Length Required',
        '412 Precondition Failed',
        '413 Request Entity Too Large',
        '414 Request-URI Too Long',
        '415 Unsupported Media Type',
        '416 Requested Range Not Satisfiable',
        '417 Expectation Failed',
        '500 Internal Server Error',
        '501 Not Implemented',
        '502 Bad Gateway',
        '503 Service Unavailable',
        '504 Gateway Timeout',
        '505 HTTP Version Not Supported'
]

content_encodings = ['gzip', 'x-gzip', 'compress', 'x-compress', 'deflate', 'identity', 'exi', 'pack200-gzip', 'SDCH', 'bzip2', 'peerdist']
transfer_encodings = ['chunked', 'compress', 'deflate', 'gzip', 'identity']

counts = [1, 5, 17, 33, 65, 129, 257, 513, 1024, 2049, 4097, 8193, 12288]

delimiters = open("fuzzstrings/delimiters", "r")
numbers = open("fuzzstrings/numberMutators", "r")
strings = open("fuzzstrings/fuzzdb", "r")

def httpfuzz(socket):

        print "MUTATION STAGE"
        
        inputs = open("httpresponses.txt", "r")
        for line in inputs:
            mutator_char("", "", "HTTP/1.1 200 OK\r\n", line.strip("\r\n") + "\r\n\r\n", "http", 0, socket)
            mutator_delimiter("", "", "HTTP/1.1 200 OK\r\n", line.strip("\r\n") + "\r\n\r\n", "http", 0, socket)
            for number in numbers:
                send_http_response(socket, "HTTP/1.1 200 OK\r\n" + mutator_number(line.strip("\r\n"), number) + "\r\n\r\n")
        
        print "GENERATION STAGE"

        print "Fuzzing strings are sent as a response"
        for line in strings:
            for c in counts:
                send_http_response(socket, int(c)*line.strip("\r\n"))
                send_http_response(socket, int(c)*line)

        #----------------------------------------------------------------------------------------------------------

        print "Fuzzing strings are used as response headers"

        for line in strings:
            for c in counts:
                send_http_response(socket, "HTTP/1.1 200 OK\r\n" + int(c)*line.strip("\r\n")+": default"+"\r\n\r\n")

        #----------------------------------------------------------------------------------------------------------

        print "Custom HTTP version"

        for line in numbers:
            send_http_response(socket, "HTTP/" + line.strip("\r\n") + "." + line.strip("\r\n") + " 200 OK\r\n\r\n")

        for line in strings:
            for c in counts:
                send_http_response(socket, int(c)*line.strip("\r\n") + " 200 OK\r\n" "header: default"+"\r\n\r\n")

        #----------------------------------------------------------------------------------------------------------

        # All headers are concatinated and sent to target in response (with argument set to random)

        print "all headers at once..."
        data = ""
        for header in headers:
            data = data + header + ": random\r\n"
        send_http_response(socket, "HTTP/1.1 200 OK\r\n" + data + "\r\n")

        #----------------------------------------------------------------------------------------------------------

        # Compression header is set and fuzzing string is sent as a header
        
        print "Compression header"
        for header in headers:
            for line in strings:
                for c in counts:
                    for encoding in content_encodings:
                        send_http_response(socket, "HTTP/1.1 200 OK\r\nContent-Encoding: " + encoding + "\r\n" + header + ": " + c*line.strip("\r\n") + "\r\n\r\n")
                        send_http_response(socket, "HTTP/1.1 200 OK\r\nContent-Encoding: gzip\r\n" + c*line.strip("\r\n") + ": random\r\n\r\n")

        #----------------------------------------------------------------------------------------------------------

        # Header and header argument forging
        
        print "Header forging"
        for header in headers:
                
                for line in strings:
                    for c in counts:
                        send_http_response(socket, "HTTP/1.1 200 OK\r\n"+header+": " + int(c)*line.strip("\r\n") + "\r\n\r\n")
                
                for line in strings:
                    for c in counts:
                        send_http_response(socket, "HTTP/1.1 200 OK\r\n" + int(c)*line.strip("\r\n") + "\r\n" + header + ": " + int(c)*line.strip("\r\n") + "\r\n\r\n")

        #----------------------------------------------------------------------------------------------------------

        # header specific fuzzing and 

        print "Header specific"
        
        for encoding in content_encodings:
            send_http_response(socket, "HTTP/1.1 200 OK\r\nContent-Encoding: " + encoding*1000 + "\r\n\r\n")
            send_http_response(socket, "HTTP/1.1 200 OK\r\nContent-Encoding: " + encoding*10000 + "\r\n\r\n")
            send_http_response(socket, "HTTP/1.1 200 OK\r\nContent-Encoding: " + (encoding + ";")*1000 + "\r\n\r\n")

        for encoding in transfer_encodings:
            send_http_response(socket, "HTTP/1.1 200 OK\r\nTransfer-Encoding: " + encoding*1000 + "\r\n\r\n")
            send_http_response(socket, "HTTP/1.1 200 OK\r\nTransfer-Encoding: " + encoding*10000 + "\r\n\r\n")
            send_http_response(socket, "HTTP/1.1 200 OK\r\nTransfer-Encoding: " + encoding + "; " + (encoding + "=\"mp3\"; ")*1000 + encoding + "=\"mp3\"" + "\r\n\r\n")

        for line in strings:
            for c in counts:
                send_http_response(socket, "HTTP/1.1 200 OK\r\nSet-Cookie: Password=" + int(c)*line.strip("\r\n") + "\r\n\r\n")            
                    
        for header in headers_date:
            for delimiter in delimiters:
                send_http_response(socket, "HTTP/1.1 200 OK\r\n" + header + ": Wed, 11 Aug 2010 10"+delimiter.strip("\r\n")+"04"+delimiter.strip("\r\n")+"31 GMT" + "\r\n\r\n")

        for header in headers_number:
            for line in numbers:
                send_http_response(socket, "HTTP/1.1 200 OK\r\n"+header+": " + line.strip("\r\n") + "\r\n\r\n")

            for line in strings:
                for c in counts:
                    send_http_response(socket, "HTTP/1.1 200 OK\r\n"+header+": " + int(c)*line.strip("\r\n") + "\r\n\r\n")

            for line in counts:
                send_http_response(socket, "HTTP/1.1 200 OK\r\n"+header+": " + line*'A' + "\r\n\r\n")

        for header in headers_address:
            for delimiter in delimiters:
                send_http_response(socket, "HTTP/1.1 200 OK\r\n"+header+": www"+delimiter.strip("\r\n")+"user" + delimiter.strip("\r\n") + "gmail"+delimiter.strip("\r\n")+"com\r\n\r\n")

        #----------------------------------------------------------------------------------------------------------

        #Other response codes
        
        print "Response codes fuzzing"

        for line in strings:
            for code in response_codes:
                for c in counts:
                    send_http_response(socket,"HTTP/1.1 " + code + "\r\n" + int(c)*line.strip("\r\n") + "\r\n\r\n")

        for line in counts:
            for code in response_codes:
                send_http_response(socket,"HTTP/1.1 " + code + "\r\n" + line*'A' + "\r\n\r\n")

        for line in numbers:
            send_http_response(socket,"HTTP/1.1 " + line.strip("\r\n") + "\r\n" + "text" + "\r\n\r\n")
        
        #----------------------------------------------------------------------------------------------------------
