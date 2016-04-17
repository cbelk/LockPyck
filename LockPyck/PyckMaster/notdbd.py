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

# This file contains an implementation of the NotDBD algorithm proposed by Trey Watford.
# The basic idea behind the algorithm is is to generate all preterminals by keeping the
# last non-terminal in the production as the only non-terminal in the pre-terminal. An 
# implementation of the Cartesian Preterms algorithm proposed by Christian Belk is also
# in the file. The idea behind this algorithm is detailed above it's implementation. It
# also contains the functions for adding/removing elements from the preterm queue.
#
# Author: Christian Belk

import gc
import os
import sys
import time
import operator
import itertools
import freak_roundup
try:
    import psutil
except:
    print '[-] The psutil module is required.\n[-] You can use a package manager to install it (e.g. pip install psutil).'
    sys.exit()

# This function takes a list of pre-terminals and the queue. Then each pre-terminal in the list is 
# appended to the queue.
def addToQueue (pretermlist, queue):
    for preterm in pretermlist:
        queue.put(preterm)
    return

# This function takes the queue. It then empties the contents of the queue into a list which is then returned.
def dumpQueue (queue):
    preterms = []
    while not queue.empty():
        preterms.append(queue.get())
    return preterms

# This function produces a preterm by concatenating the elements at each index in the respective set.
def getPartialTerminal (sets, indexes):
    partTerm = ''
    for i in xrange(len(indexes)):
        partTerm += sets[i][indexes[i]]
    return partTerm

# This function determines if all the elements from the cartesian product have been generated by checking if
# the indexes are equal to their respective lengths - 1.
def weDoneYet (lengths, indexes):
    for i in xrange(len(indexes)):
        if indexes[i] < (lengths[i] - 1):
            return False
    return True

# This function takes a list of lists (the sets), the queue, and the non-term. It then generates the cartesian
# product by first initializing the index for all sets to 0 (which is the first element in the product). 
# Then starting with the last set, it increments the index, each time generating a new element in the product.
# Everytime a new element in the product is generated, it is made into a preterm and added to the queue. When 
# the current set index can't be incremented anymore (ie the last element in that set has been used), curr_index 
# is set to the index of the next set down in the list, that set's index is incremented and the indexes of all 
# sets higher in the list than the current one are reset to 0 (whch is the next element in the product). The 
# process is then repeated starting with incrementing the last set.
def cartesianPreterms (sets, queue, nonterm):
    lengths = []
    indexes = []
    THRESHOLD = 80
    for s in sets:
        lengths.append(len(s))
        indexes.append(0)
    curr_ind = len(indexes) - 1
    while True:
        ram = psutil.virtual_memory()
        swp = psutil.swap_memory()
        while ram.percent > THRESHOLD:
            if swp.total == 0:
                print '[!] CartesianPreterms: Taking a break since memory usage is high ...'
                time.sleep(30)
            elif swp.percent > THRESHOLD:
                print '[!] CartesianPreterms: Taking a break since memory usage is high ...'
                time.sleep(30)
            else:
                break
            ram = psutil.virtual_memory()
            swp = psutil.swap_memory()
        partTerm = getPartialTerminal(sets, indexes)
        queue.put([partTerm, nonterm])
        if weDoneYet(lengths, indexes):
            break
        if indexes[curr_ind] < lengths[curr_ind]:
            indexes[curr_ind] += 1
        if indexes[curr_ind] == lengths[curr_ind]:
            curr_ind -= 1
            while curr_ind >= 0 and indexes[curr_ind] + 1 == lengths[curr_ind]:
                curr_ind -= 1
            indexes[curr_ind] += 1
            curr_ind += 1
            while curr_ind < len(indexes):
                indexes[curr_ind] = 0
                curr_ind += 1
            curr_ind -= 1
    return

# This function takes the path to the FreakSheets directory. It uses seqs to get the sequences (string) 
# in descending order of frequency, and uses ndbd_dict to map the string version of the sequence to its
# list representation. The last element in the list representation will be the non-term in the pre-term
# and is chopped off (to be added back to the final pre-term). Every other non-terminal in the sequence
# is reduced to a list containing all its terminals. These list are passed to the cartesianPreterms 
# method to have the pre-terms generated and added to the queue.
def notdbd (FREAKBASE, queue):
    seqs = freak_roundup.sortaFreaky(os.path.join(FREAKBASE, 'Seq.freak'))
    ndbd_dict = freak_roundup.getMeThatFreak(os.path.join(FREAKBASE, 'NDBD.freak'))
    THRESHOLD = 80
    if seqs and ndbd_dict:
        print '[+] Notdbd: Generating preterms now ...'
        for seq, freak in seqs:
            ram = psutil.virtual_memory()
            swp = psutil.swap_memory()
            while ram.percent > THRESHOLD:
                if swp.total == 0:
                    print '[!] Notdbd: Taking a break since memory usage is high ...'
                    time.sleep(30)
                elif swp.percent > THRESHOLD:
                    print '[!] Notdbd: Taking a break since memory usage is high ...'
                    time.sleep(30)
                else:
                    break
                ram = psutil.virtual_memory()
                swp = psutil.swap_memory()
            if seq != 'freakycount':
                nontermlist = ndbd_dict[seq]
                nonterm = nontermlist[len(nontermlist) - 1]
                del nontermlist[-1]
                reslist = []
                i = 0
                for nterm in nontermlist:
                    sorted_freak = freak_roundup.sortaFreaky(os.path.join(FREAKBASE, nterm[0], '%s.freak' % nterm))
                    nt = [freak[0] for freak in sorted_freak]
                    del sorted_freak
                    nt.remove('freakycount')
                    reslist.append(nt)
                    del nt
                    i += 1
#                    print nt
#                print reslist
                cartesianPreterms(reslist, queue, nonterm)
                del reslist
                del nonterm
#                gc.collect()
#                permlist = list(itertools.product(*reslist))
#                print permlist
#                del reslist
#                gc.collect()
#                pretermlist = []
#                for tup in permlist:
#                    termpart = ''
#                    for term in tup:
#                        termpart += str(term)
#                    del tup
#                    pretermlist.append([termpart, nonterm])
#                del permlist
#                gc.collect()
#                print pretermlist
#                addToQueue(pretermlist, queue)
#                del pretermlist
#                gc.collect()
    print '[+] Notdbd: Generated all preterms'
    queue.put('kcyPkcoL')
    return
