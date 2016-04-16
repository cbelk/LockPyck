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
# last non-terminal in the production as the only non-terminal in the pre-terminal. The 
# claim is that this approach prevents a given preterminal from being generated mutliple
# times and may be more effecient than the dead beat dad algorithm. 

import gc
import os
import operator
import itertools
import freak_roundup

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
        print '[+] Notdbd: Generating preterms now ...'
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
    print '[+] Notdbd: Generated all preterms'
    return
