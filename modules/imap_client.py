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

imap_commands = [
    'append',
    'authenticate',
    'capability',
    'check',
    'close',
    'comparator',
    'compress',
    'conversions',
    'copy',
    'create',
    'delete',
    'deleteacl',
    'examine',
    'expunge',
    'fetch',
    'getacl',
    'getmetadata',
    'getquota',
    'getqouotaroot',
    'idle',
    'list',
    'listrights',
    'login',
    'logout',
    'lsub',
    'myrights',
    'noop',
    'notify',
    'rename',
    'search',
    'select',
    'setacl',
    'setmetadata',
    'setquota',
    'sort',
    'starttls',
    'status',
    'store',
    'subscribe',
    'thread',
    'uid',
    'unselect',
    'unsubscribe',
    'X'
]

imap_commands_onearg = [
    'authenticate',
    'select',
    'examine',
    'create',
    'delete',
    'subscribe',
    'unsubscribe'
]

imap_commands_twoarg = [
    'login',
    'rename',
    'list',
    'lsub'
]

imap_status_messages = [
    'MESSAGES',
    'RECENT',
    'UIDNEXT',
    'UIDVALIDITY',
    'UNSEEN'
]

strings = open("fuzzstrings/fuzzdb","r")
numbers = open("fuzzstrings/numberMutators","r")
delimiters = open("fuzzstrings/delimiters","r")

counts = [0, 1, 5, 17, 33, 65, 129, 257, 513, 1025, 2049, 4097, 8193, 12288]

def imapfuzz_client(host, port, fuzztype):

	if fuzztype == "response":
	    while True:
	        send_imap_request(host, port, login, password, ". list\r\n", "random")
	else:
	    print "MUTATION STAGE"

	    # Same principle as in HTTP fuzzing stage

	    imapfile = open("imaprequests.txt", "r")


	    for line in imapfile:
	        mutator_char(host, port, "a ", line, "imap")
	        mutator_delimiter(host, port, "a ", line, "imap")
	        numbers.seek(0)
	        for number in numbers:
	            send_imap_request_special(host, port, login, password, mutator_number(line, number.strip("\r\n")))    

	    #----------------------------------------------------------------------------------------------------------    

	    print "GENERATION STAGE"

	    # Arguments of commands are fuzzed

	    print "primitive argument fuzzing..."
	    for line in strings:
	        for c in counts:
	            for command in imap_commands:
	                if command in imap_commands_twoarg:
	                    send_imap_request(host, port, login, password, command, c*line.strip("\r\n"), 2, c*line.strip("\r\n"))
	                else:
	                    send_imap_request(host, port, login, password, command, c*line.strip("\r\n"), 1)

	    #----------------------------------------------------------------------------------------------------------    

	    # Fuzzing strings are sent to target without authentication

	    print "noauth fuzzing..."
	    for line in strings:
	        for c in counts:
	            sock = socket.socket()
	            sock.connect((host, int(port)))
	            sock.send("a  " + int(c)*line.strip("\r\n") + "\r\n")
	            time.sleep(0.1)
	            sock.close()

	    #----------------------------------------------------------------------------------------------------------    

	    # id of messages is fuzzed

	    print "id fuzzing..."
	    for line in strings:
	        for c in counts:
	            sock = socket.socket()
	            sock.connect((host, int(port)))
	            sock.send(int(c)*line.strip("\r\n") + " login root@root.com toor\r\n")
	            sock.recv(4096)
	            sock.send(int(c)*line.strip("\r\n") + " status random\r\n")
	            #sock.recv(4096)
	            time.sleep(0.1)
	            sock.close()

	    for line in delimiters:
	        for c in counts:
	            sock = socket.socket()
	            sock.connect((host, int(port)))
	            sock.send(int(c)*line.strip("\r\n") + " login root@root.com toor\r\n")
	            sock.recv(4096)
	            sock.send(int(c)*line.strip("\r\n") + " status random\r\n")
	            #sock.recv(4096)
	            time.sleep(0.1)
	            sock.close()

	    #----------------------------------------------------------------------------------------------------------    

	    # Fuzzing strings are used as commands

	    print "command forgin ..."
	    for line in counts:
	        send_imap_request(host, port, login, password, line*'A', "arg", 1)
	        send_imap_request(host, port, login, password, line*'A', "arg1", 2, "arg2")

	    for line in strings:
	        for c in counts:
	            send_imap_request(host, port, login, password, c*line.strip("\r\n"),"arg", 1)
	            send_imap_request(host, port, login, password, c*line.strip("\r\n"), "arg1", 2, "arg2")

	    for line in delimiters:
	        for c in counts:
	            send_imap_request(host, port, login, password, c*line.strip("\r\n"),"arg", 1)
	            send_imap_request(host, port, login, password, c*line.strip("\r\n"), "arg1", 2, "arg2")

	    #----------------------------------------------------------------------------------------------------------    

	    # Commands are repeated various times

	    print "repeating phase..."
	    for command in imap_commands:
	        for c in counts:
	            send_imap_request(host, port, login, password, int(c)*command,"arg", 1)

	    #----------------------------------------------------------------------------------------------------------    