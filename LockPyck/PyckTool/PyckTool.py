#!/usr/bin/env_python

import socket
import csv
import hashlib  #used for hashing


#constants for tcp connection
TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024

#signal messages
GET_MSG = 'get-pre-term'
CLOSE_MSG = 'close'
SUCCESS_MSG = 'success ' #space is necessary
PW_FILE_MSG = 'get-pw-file'

#function requests pre-terminal from master and returns pre-term as string
#pre-terminals are strings with one variable of a specified length
def getPretermList():
    #create TCP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    #send get preterm message
    s.send(GET_MSG)
    #get pre-terminal string (space delimited)
    pretermStr = s.recv(BUFFER_SIZE)
    s.close()   #close connection
    print 'pre-terminal string received: ', pretermStr
    #convert string to list
    print 'converting to list...'
    pretermList = pretermStr.split(' ')
    print 'done.'
    return pretermList

#function to kill master (stop master from waiting for messages)
def killMaster():
    #tell server to close its connection
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.send(CLOSE_MSG)
    s.close()
    return

#function sends success message to master
#message format = "success cypherText plainText"
def sendSuccess( pt, ct ):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.send(SUCCESS_MSG+ct+' '+pt)
    s.close()
    return

#function hashes a particular string using md5 alogrithm and returns hex
#representation of hashed string
def hashString( str ):
    m = hashlib.md5()
    m.update(str)
    return m.hexdigest()

#returns non-terminal from specified list
def getNonTerminal( lst ):
    for s in lst:
        #non-terminals must be at least length 2
        #and have a letter followed by a digit
        if len(s) >= 2 and s.split()[0][0].isalpha() and s.split()[0][1].isdigit():
            return s
    return

#function requests absolute path to password file from master
def getPwFile():
    #create TCP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    #send get preterm message
    s.send(PW_FILE_MSG)
    #get password file path
    filePath = s.recv(BUFFER_SIZE)
    s.close()   #close connection
    print 'password file path received: ', filePath
    return filePath

#driver for PyckTool
def main():
    #get pre-terminal list
    preterm = ['!','L2','!'];
    print 'preterminal list: '
    print preterm
    #extract variable from pre-term
    nt = getNonTerminal(preterm)
    print 'non terminal: '+nt+'\n'
    #open associated freak sheet for processing
    with open('../../FreakSheets/'+nt.split()[0][0]+'/'+nt+'.freak', 'rb') as infile:
        reader = csv.reader(infile, delimiter=',', quotechar='|')
        firstLine = True
        for row in reader:
            if firstLine:  #skip first line
                firstLine = False
                continue
            else:
                #create plain text string by replacing non-terminal with row
                plainText = ''.join(preterm)
                plainText = plainText.replace(nt,row[0])
                #print new plain text password possibility
                print 'plain text word ', plainText
                #hash possible password
                hashedStr = hashString(plainText)
                print 'Hex Hashed password (md5): ', hashedStr
                #get password file path from master
                pwfp = getPwFile()
                #compare hash to file (check for match)
                with open(pwfp, 'rb') as pwFile:
                    found = False
                    rdr = csv.reader(pwfp, delimeter=',', quotechar='|')
                    #loop through password file comparing hashes
                    for line in rdr:
                        #if found exit loop
                        if found == True:
                            break
                        else:
                            if line == hashedStr:   # compare hashed pw to line
                                found = True
                                #message success to master
                                sendSuccess(plainText, hashedStr)

    return #main function return

if __name__ == "__main__":
	main()
