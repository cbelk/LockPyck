#!/usr/bin/env_python

#########################################################################################
#                                                                                       #
#    LockPyck -- A Password Cracker Powered By Probabilistic Context free grammars      #
#    Copyright (C) 2016  Christian Belk -- cbelk88@gmail.com                            #
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

# This file contains the notdbd function which prepares the data to be processed by the
# cartesianPreterms function.
#
# Author: Christian Belk

import os
import qutility
import utility
from cartesianPreterms import cartesianPreterms
from FreakMaster import freak_roundup

# notdbd takes the path to the FreakSheets directory. It uses seqs to get the sequences (string) 
# in descending order of frequency, and uses ndbd_dict to map the string version of the sequence to its
# list representation. The last element in the list representation will be the non-term in the pre-term
# and is chopped off (to be added back to the final pre-term). Every other non-terminal in the sequence
# is reduced to a list containing all its terminals. These list are passed to the cartesianPreterms 
# method to have the pre-terms generated and added to the queue.
def notdbd(FREAKBASE, queue, poison_queue, poison_pill, pill_count):
    seqs = freak_roundup.sortaFreaky(os.path.join(FREAKBASE, 'Seq.freak'))
    ndbd_dict = freak_roundup.getMeThatFreak(os.path.join(FREAKBASE, 'NDBD.freak'))
    THRESHOLD = 80
    if seqs and ndbd_dict:
        print '[+] Notdbd: Generating preterms now ...'
        for seq, freak in seqs:
            if qutility.poisoned(poison_queue):
                print '[+] Notdbd: Recieved poison pill! Terminating ...'
                return
            utility.courtesyCheck(THRESHOLD)
            if seq != 'freakyc0unt':
                nontermlist = ndbd_dict[seq]
                nonterm = '%s%s' % (nontermlist[len(nontermlist) - 2], nontermlist[len(nontermlist) - 1])
                del nontermlist[-2:]
                reslist = []
                i = 0
                while True:
                    if i >= len(nontermlist):
                        break
                    sorted_freak = freak_roundup.sortaFreaky(os.path.join(FREAKBASE, nontermlist[i], '%s%s.freak' % (nontermlist[i], nontermlist[i+1])))
                    nt = [freak[0] for freak in sorted_freak]
                    del sorted_freak
                    nt.remove('freakyc0unt')
                    reslist.append(nt)
                    del nt
                    i += 2
                if reslist:
                    cartesianPreterms(reslist, queue, poison_queue, nonterm)
                else:
                    queue.put([nonterm])
                del reslist
                del nonterm
    print '[+] Notdbd: Generated all preterms ...'
    print '[+] Notdbd: Poisoning other LockPyck processes ...'
    qutility.poison(queue, poison_pill, pill_count)
    print '[+] Notdbd: Terminating ...'
    return
