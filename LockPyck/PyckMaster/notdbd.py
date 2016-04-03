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
import gc
import os
import operator
import itertools
import freak_roundup

#global list used to hold pre-terms to be used by pyckTools
#items in list are not in order or priority
#globalList = []
#
#function add to global list adds a list of pre-terminals to the list
#def addToGlobal( ptList ):
#    globalList.extend( ptList )
#    return
#
#empties global list and returns a list of lists (pre-terminals) in the format
#[['someTextHere', 'L8'],['someothertextHere', 'S3'] ]
#def emptyGlobal():
#    preTerms = []
#    for x in range(0, len(globalList)-1):
#        preTerms.append(globalList[x][0])
#    del globalList[:]
#    return preTerms
#
#
#notdbd takes a sequence (a list of non-terminals and an associated frequency) and
#the path to the FreakSheets Directory as arguments
#the algorithm generates all permutations of a password with a single non-terminal at
#the right end. The list of permutations and their associated frequencies is added
#to the global list for use by the PyckTools
#def notdbd( seqList, freaksPath):
#    resultList = []
#    #loop through sequence non-terminals excluding the last one
#    for x in range(0,len(seqList[0])-1):
#        #replace non-terminals in sequence list with a list of terminals
#        fp = freaksPath+seqList[0][x][0]+'/'+seqList[0][x]+'.freak'
#        #call sortaFreaky from freak_roundup file to get tmp list
#        tmp = freak_roundup.sortaFreaky(fp)
#        seqList[0][x] = tmp[1:len(tmp)-1]
#    #calculate number of results in result list
#    numResults = 1
#    for x in range(0, len(seqList[0])):
#        numResults = numResults* (len(seqList[0][x]))
#    #initialize empty list of length numResults
#    for x in range(0, numResults-1):
#        temp = [[''],1]
#        resultList.append(temp)
#
#    #generate all permutations excluding the non-terminal at end
# #   for x in range(0, len(seqList[0])-1):#loop through lists
# #       if len(seqList[0][x]) > 1: #process lists
# #           for i in range(0, len(resultList)):
#                #append terminal a number of strings in result
# #               resultList[i][0][0] +=seqList[0][x][i%len(seqList[0][x])][0]
#                #multiply freaks for priority
# #               resultList[i][1] *=seqList[0][x][i%len(seqList[0][x])][1]
#    #append non-terminal to end of each entry
# #   for x in range(0, len(resultList)):
# #       resultList[x][0].append(seqList[0][len(seqList[0])-1])
# #       resultList[x][1] *= seqList[0][1][1] #multiply freak by sequence freak
#    
#    #add result list to global list
# #   addToGlobal( resultList )
#    #return from function
# #   return

def addToQueue (pretermlist, queue):
    for preterm in pretermlist:
        queue.put(preterm)
    return

def dumpQueue (queue):
    preterms = []
    while not queue.empty():
        preterms.append(queue.get())
    return preterms

# This function takes the path to the FreakSheets directory. It uses seqs to get the sequences (string) 
# in descending order of frequency, and uses ndbd_dict to map the string version of the sequence to its
# list representation. The last element in the list representation will be the non-term in the pre-term
# and is chopped off (to be added back to the final pre-term). Every other non-terminal in the sequence
# is reduced to a list containing all its terminals. These list are passed to the builtin permutations
# function which returns a list of tuples (each representing a permutation). The preterminal (list) is
# then formed and appended to pretermlist which gets passed to addToGlobal.
def notdbd (FREAKBASE, queue):
    seqs = freak_roundup.sortaFreaky(os.path.join(FREAKBASE, 'Seq.freak'))
    ndbd_dict = freak_roundup.getMeThatFreak(os.path.join(FREAKBASE, 'NDBD.freak'))
    if seqs and ndbd_dict:
        print '[+] notdbd: Generating preterms now ...'
        for seq, freak in seqs:
            if seq != 'freakycount':
                nontermlist = ndbd_dict[seq]
                nonterm = nontermlist[len(nontermlist) - 1]
                del nontermlist[-1]
                reslist = []
                i = 0
                for nterm in nontermlist:
                    sorted_freak = freak_roundup.sortaFreaky(os.path.join(FREAKBASE, nterm[0], '%s.freak' % nterm))
                    nt = [freak[0] for freak in sorted_freak]
                    nt.remove('freakycount')
                    reslist.append(nt)
                    del nt
                    i += 1
#                    print nt
#                print reslist
                permlist = list(itertools.product(*reslist))
#                print permlist
                del reslist
                gc.collect()
                pretermlist = []
                for tup in permlist:
                    termpart = ''
                    for term in tup:
                        termpart += str(term)
                    del tup
                    pretermlist.append([termpart, nonterm])
                del permlist
                gc.collect()
#                print pretermlist
                addToQueue(pretermlist, queue)
                del pretermlist
                gc.collect()
    print '[+] notdbd: Generated all preterms'
    return
