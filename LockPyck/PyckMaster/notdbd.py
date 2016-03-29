#!/usr/bin/env_python

#########################################################################################
#                                                                                       #
#    LockPyck -- A Password Cracker Powered By Probabilistic Context free grammars      #
#    Copyright (C) 2016  Christian Belk -- cbelk88@gmail.com                            #
#                        Trey Watford   -- treyjustinwatford@gmail.com                  #
#                                                                                       #
#    This program is free software: you can redistribute it and/or modify               #
#    it under the terms of the GNU General Public License as published by               #
#    the Free Software Foundation, either version 3 of the License, or                  #
#    (at your option) any later version.                                                #
#                                                                                       #
#    This program is distributed in the hope that it will be useful,                    #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of                     #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                      #
#    GNU General Public License for more details.                                       #
#                                                                                       #
#    You should have received a copy of the GNU General Public License                  #
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.              #
#                                                                                       #
#########################################################################################

#necessary imports
import os
import operator
import Queue
try:
    import cPickle as pickle
except:
    import pickle

#global priority queue used to hold pre-terms to be used by pyckTools
#items in queue are prioritized based on frequency
gloablQueue = Queue.PriorityQueue()


#function takes a sequence as a string and returns the list representation of the
#sequence with each non-terminal as its own string
def strToList( seq ):
    count = 0
    index = len(seq)-1
    tmp = []
    while(len(seq)>0):
        count = count+1
        if(seq[index].isalpha()):
            tmp.append(seq[index:]) #append substring to list
            seq=seq[:-count]
            count = 0
        index = index-1
    tmp.reverse();  #reverse list so that non-terms are in correct order
    return tmp

# This function takes the path to a freaksheet. It un-pickles it, and passes it to sorted,
# which returns a sorted list of tuples.
def sortaFreaky(freaksheet):
    if os.path.isfile(freaksheet):
        with open(freaksheet, 'rb') as freakin:
            print freaksheet +' opened success'
            stale_pickle = pickle.load(freakin)
        freakin.close()
        return sorted(stale_pickle.items(), key=operator.itemgetter(1), reverse=True)
    return



#notdbd takes a sequence (a list of non-terminals and an associated frequency) and
#the path to the FreakSheets Directory as arguments
#the algorithm generates all permutations of a password with a single non-terminal at
#the right end. The list of permutations and their associated frequencies is returned
def notdbd( seqList, freaksPath):

    resultList = []
    #loop through sequence non-terminals excluding the last one
    for x in range(0,len(seqList[0])-1):
        #replace non-terminals in sequence list with a list of terminals
        fp = freaksPath+seqList[0][x][0]+'/'+seqList[0][x]+'.freak'
        tmp = sortaFreaky(fp)
        seqList[0][x] = tmp[1:len(tmp)]
    #calculate number of results in result list
    numResults = 1
    for x in range(0, len(seqList[0])):
        numResults = numResults* (len(seqList[0][x]))
    #initialize empty list of length numResults
    for x in range(0, numResults-1):
        temp = ["",1]
        resultList.append(temp)

    #generate all permutations excluding the non-terminal at end
    for x in range(0, len(seqList[0])-1):#loop through lists
        if len(seqList[0][x]) > 1: #process lists
            for i in range(0, len(resultList)):
                #append terminal a number of strings in result
                resultList[i][0] +=seqList[0][x][i%len(seqList[0][x])][0]
                #multiply freaks for priority
                resultList[i][1] *=seqList[0][x][i%len(seqList[0][x])][1]
    #append non-terminal to end of each entry
    for x in range(0, len(resultList)):
        resultList[x][0] +=seqList[0][len(seqList[0])-1]
        resultList[x][1] *= seqList[0][1][1] #multiply freak by sequence freak
    #return resulting list
    return resultList


#driver function used for testing
def main():
    #we need to replace these hard coded paths
    pathToFreaks = '/home/trey_watford/lockpyck/LockPyck/FreakSheets/'
    seqs = sortaFreaky('/home/trey_watford/lockpyck/LockPyck/FreakSheets/Seq.freak')
    seqList = []
    #convert all sequences to lists
    print 'converting sequences to lists\n'
    for x in range(1, len(seqs)):
        temp = []
        temp.append(strToList(seqs[x][0]))    #replace string with sequence
        temp.append(seqs[x][1])
        seqList.append(temp)
    print '[+] sequences converted'
    print 'calling notdbd on each sequence'
    for x in range(0, len(seqList)-1):
        preTermList = notdbd(seqList[x], pathToFreaks )
        #print preTermList for testing purposes
        #for x in range(0, len(preTermList)-1):
            #print preTermList[x]
    return


if __name__ == "__main__":
    main()
