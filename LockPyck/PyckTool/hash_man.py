#! /usr/bin/env python

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

# This file contains the functions for the hash_man daemon.
#
# Author: Christian Belk

import datetime
import os
import qutility
import time
import utility
from FreakMaster import freak_roundup
from FreakMaster import seq_help

# manage is run in the hash_man daemon to manage the hashlist and the writing to the cracked
# file. It terminates by either all of the hashes getting cracked in which case it poisons
# the poison_queue or by receiving a poison pill in the poison_queue (meaning all of the
# password guesses have been generated) in which case it checks the suc_queue one last time
# and writes any successes.
def manage(crackedfile, hashlist, suc_queue, poison_queue, poison_pill, pill_count, fsheets, verbose):
    poisoned = False
    with open(crackedfile, 'a+') as crackedout:
        crackedout.write('LockPyck run on %s\n' % datetime.datetime.now())
        while hashlist:
            tupls = []
            success = qutility.dumpQueue(suc_queue)
            for succ in success:
                print '\n[+] Hash: %s  ||  Password: %s\n' % (succ[0], succ[1])
                crackedout.write('[+] Hash: %s  ||  Password: %s\n' % (succ[0], succ[1]))
                tupls.append(seq_help.seqCreator(succ[1]))
                c = hashlist.count(succ[0])
                while c > 0:
                    hashlist.remove(succ[0])
                    c -= 1
            if tupls:
                update(tupls, fsheets, verbose)
            if poisoned:
                crackedout.close()
                print '[+] Hash_Man: Terminating ...'
                return
            if qutility.poisoned(poison_queue):
                print '[+] Hash_Man: Recieved poison pill!'
                print '[+] Hash_Man: Checking for successes one last time ...'
                poisoned = True
            else:
                time.sleep(5)
    crackedout.close()
    print '[+] Cracked all hashes !!!'
    print '[+] Hash_Man: Poisoning other LockPyck processes ...'
    qutility.poison(poison_queue, poison_pill, pill_count)
    print '[+] Hash_Man: Terminating ...'
    return

# update is used by hash_man to feed the successfully cracked passwords through the learning
# phase and update the freaksheets. The NDBD freaksheet does not get updated since the sequence
# already exist in there and it doesn't keep an actual frequency count.
def update(tupls, fsheets, verbose):
    sqfreak = os.path.join(fsheets, 'Seq.freak')
    seq_dict = {'freakyc0unt' : 0}
    terminal_dict = {}
    for tupl in tupls:
        seqString = tupl[0]
        seq = tupl[1]
        pswd = tupl[2]
        terminal_dict = freak_roundup.updateTerminals(seq, pswd, terminal_dict)
        if seqString in seq_dict:
            seq_dict[seqString] += 1
        else:
            seq_dict[seqString] = 1
        seq_dict['freakyc0unt'] += 1
    freak_roundup.freakyUpdate(sqfreak, seq_dict, verbose)
    for freakfile, terminalSeq in terminal_dict.iteritems():
        freak_roundup.freakyCreator((freakfile, terminalSeq, fsheets, verbose))
    return
