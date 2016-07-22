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

from deprecated.modules.functions import *

delimiters = open("fuzzstrings/delimiters", "r")
numbers = open("fuzzstrings/numberMutators", "r")
strings = open("fuzzstrings/stringMutators", "r")

imap_responses = [
    'OK',
    'NO',
    'BAD',
    'PREAUTH',
    'BYE',
    'CAPABILITY',
    'LIST',
    'LSUB',
    'STATUS',
    'SEARCH',
    'FLAGS',
    'EXISTS',
    'RECENT',
    'EXPUNGE',
    'FETCH'
]

response_codes = [
    'UNAVAILABLE',
    'AUTHENTICATIONFAILED',
    'AUTHORIZATIONFAILED',
    'EXPIRED',
    'PRIVACYREQUIRED',
    'CONTACTADMIN',
    'NOPERM',
    'INUSE',
    'EXPUNGEISSUED',
    'CORRUPTION',
    'SERVERBUG',
    'CLIENTBUG',
    'CANNOT',
    'LIMIT',
    'OVERQUOTA',
    'ALREADYEXISTS',
    'NONEXISTENT'
    'UNDEFINED-FILTER',
    'BADEVENT',
    'NOTIFICATIONOVERFLOW',
    'METADATA',
    'NOUPDATE',
    'MAXCONVERTPARTS',
    'MAXCONVERTMESSAGES',
    'TEMPFAIL',
    'ANNOTATIONS',
    'ANNOTATE',
    'BADCOMPARATOR',
    'NOTSAVED',
    'CLOSED',
    'COMPRESSIONACTIVE',
    'MODIFIED',
    'NOMODSEQ',
    'HIGHESTMODSEQ',
    'BADURL',
    'TOOBIG',
    'URLMECH',
    'COPYUID',
    'APPENDUID',
    'UIDNOTSTICKY',
    'UNKNOWN-CTE',
    'UNSEEN',
    'UIDVALIDITY',
    'UIDNEXT',
    'TRYCREATE',
    'READ-WRITE',
    'READ-ONLY',
    'PERMANENTFLAGS',
    'PARSE',
    'BADCHARSET',
    'ALERT',
    'REFERRAL',
    'NEWNAME'

]

counts = [0, 1, 5, 17, 33, 65, 129, 257, 513, 1025, 2049, 4097, 8193, 12288]

def imapfuzz(socket):
        
        print "MUTATION STAGE"
        
        for response in imap_responses:
            print response
            mutator_char("", "", "", response, "imap", 0, socket)


        #----------------------------------------------------------------------------------------------------------
        
        print "GENERATION STAGE"
        
        # dumb fuzzing
        for line in strings:
            for c in counts:
                send_imap_response(socket, "a  OK " + int(c)*line.strip("\r\n") + "\r\n")
                send_imap_response(socket, int(c)*line.strip("\r\n") + " . OK\r\n")
        
        #----------------------------------------------------------------------------------------------------------

        # fuzzing responses
        for line in strings:
            for c in counts:
                send_imap_response(socket, "a  " + int(c)*line.strip("\r\n") + " random\r\n")

        for line in delimiters:
            for c in counts:
                send_imap_response(socket, "a  " + int(c)*line.strip("\r\n") + " random\r\n")                

        #----------------------------------------------------------------------------------------------------------

        #fuzzing response codes
        for response in imap_responses:
            for code in response_codes:
                for c in counts:
                    send_imap_response(socket, "a " + int(c)*response + " [" + code + "] random\r\n")
                    send_imap_response(socket, "a " + response + " [" + int(c)*code + "] random\r\n")

        for response in imap_responses:
            for line in strings:
                for c in counts:
                    send_imap_response(socket, "id " + response + " [" + int(c)*line.strip("\r\n") + "] random\r\n")
                    send_imap_response(socket, "id " + response + " " + int(c)*line.strip("\r\n") + " random\r\n")

            for line in delimiters:
                for c in counts:
                    send_imap_response(socket, "id " + response + " [" + int(c)*line.strip("\r\n") + "] random\r\n")
                    send_imap_response(socket, "id " + response + " " + int(c)*line.strip("\r\n") + " random\r\n")

        #----------------------------------------------------------------------------------------------------------