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

# This file contains the function for the hash_man daemon.
#
# Author: Christian Belk

import datetime
import qutility
import time
import utility

# manage is run in the hash_man daemon to manage the hashlist and the writing to the cracked
# file. It terminates by either all of the hashes getting cracked in which case it poisons
# the poison_queue or by receiving a poison pill in the poison_queue (meaning all of the
# password guesses have been generated) in which case it checks the suc_queue one last time
# and writes any successes.
def manage(crackedfile, hashlist, suc_queue, poison_queue, poison_pill, pill_count):
    poisoned = False
    with open(crackedfile, 'a+') as crackedout:
        crackedout.write('LockPyck run on %s\n' % datetime.datetime.now())
        while hashlist:
            success = qutility.dumpQueue(suc_queue)
            for succ in success:
                print '\n[+] Hash: %s  ||  Password: %s\n' % (succ[0], succ[1])
                crackedout.write('[+] Hash: %s  ||  Password: %s\n' % (succ[0], succ[1]))
                c = hashlist.count(succ[0])
                while c > 0:
                    hashlist.remove(succ[0])
                    c -= 1
            if poisoned:
                crackedout.close()
                print '[+] Hash_Man: Terminating ...'
                return
            if qutility.poisoned(poison_queue):
                print '[+] Hash_Man: Recieved poison pill!'
                print '[+] Hash_Man: Checking for successes one last time ...'
                poisoned = True
            else:
                time.sleep(10)
    crackedout.close()
    print '[+] Cracked all hashes !!!'
    print '[+] Hash_Man: Poisoning other LockPyck processes ...'
    qutility.poison(poison_queue, poison_pill, pill_count)
    print '[+] Hash_Man: Terminating ...'
    return
