#!/usr/bin/env python

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

# This file contains the sub-driver for the pycking process.
#
# Author: Christian Belk

import multiprocessing
import pyck
import qutility
import time
import utility

# This is the sub-driver for the pycking process. It retrieves the preterms from the queue and starts a pool of
# pycks to process them. Any successes returned from the pycks gets added to the suc_queue to be consumed by 
# the hash_man daemon. It terminates by receiving a poison pill in either the poison_queue (meaning hash_man
# poisoned it because all hashes are gone) or the queue (meaning notdbd poisoned it because all of the preterms
# are gone in which case it poisons the poison_queue).
def drive(hashlist, crackedfile, FREAKBASE, queue, suc_queue, poison_queue, poison_pill, pill_count, verbose):
    poisoned = False
    print '[+] Super_Pyck: Starting the pycking process ...'
    while not qutility.poisoned(poison_queue):
        preterms = qutility.dumpQueue(queue)
        if poison_pill in preterms:
            print '[+] Super_Pyck: Recieved poison pill from NotDBD!'
            print '[+] Super_Pyck: Processing any remaining preterms ...'
            poisoned = True
            preterms.remove(poison_pill)
        if preterms:
            if verbose:
                print '[+] Super_Pyck: Got some preterms and starting some pycks ...'
            pool_size = multiprocessing.cpu_count() - 1
            pool = multiprocessing.Pool(processes=pool_size, maxtasksperchild=2,)
            tupls = []
            for preterm in preterms:
                tupls.append((preterm, hashlist, FREAKBASE, verbose))
            if tupls:
                pool_outputs = pool.map(pyck.cutTheKey, tupls)
                pool.close()
                pool.join()
                del tupls
                for success in pool_outputs:
                    for succ in success:
                        suc_queue.put(succ)
                del pool_outputs
            else:
                print '[-] Super_Pyck: Error creating tuples'
                print '[-] Super_Pyck: preterm = %s  ||  hashlist = %s' % (str(preterm), str(hashlist))
                pool.close()
                pool.join()
        else:
            print '[!] Super_Pyck: Taking a break since no preterms are available right now ...'
            if not poisoned:
                time.sleep(5)
        if poisoned:
            print '[+] Super_Pyck: Poisoning other LockPyck processes ...'
            qutility.poison(poison_queue, poison_pill, pill_count)
            break
    print '[+] Super_Pyck: Terminating ...'
    return
