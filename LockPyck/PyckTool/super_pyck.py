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
# The data structures:
# cracked => key = hash; value = list of plaintext(s) that hashed to the key hash
#
# Author: Christian Belk

import multiprocessing
import pyck
import time
import qutility
import utility as util
from NDBD import utility as nutil

# This is the sub-driver for the pycking process. It keeps looping as long as there are hashes to be
# cracked, getting the preterms from the global list and starting a pool of pyck workers to do some cracking.
def drive (hashfile, crackedfile, FREAKBASE, queue, suc_queue, poison_queue, poison_pill, pill_count, verbose):
    print '[+] Super_pick: Reading hashes from %s ...' % hashfile
    hashlist = util.getThoseHashes(hashfile)
    cracked = {}
    THRESHOLD = 80
    crackedTemp = '%s~' % crackedfile
    poisoned = False
    print '[+] Super_Pyck: Starting the pycking process ...'
    while not qutility.poisoned(poison_queue):
        preterms = nutil.dumpQueue(queue)
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

# updateCrackedPasses takes a list of successful cracks (plaintext) and the hashlist. It then adds the hashed
# passwords as the key to the cracked dict and the plaintext into the list (value). Note: list is used
# since collision is possible with random user created passwords (though very, very low probability).
# **Might need to take out the code that removes the hash from hashlist to allow for collision***
def updateCrackedPasses (success, hashlist, cracked, crackedTemp):
    with open(crackedTemp, 'a+') as crackedout:
        for suc in success:
            crackedout.write('[+] %s  ==>  %s\n' % (suc[0], suc[1]))
            if suc[0] in cracked:
                cracked[suc[0]].append(suc[1])
            else:
                cracked[suc[0]] = [suc[1]]
                c = hashlist.count(suc[0])
                while c > 0:
                    hashlist.remove(suc[0])
                    c -= 1
    crackedout.close()
    return hashlist
