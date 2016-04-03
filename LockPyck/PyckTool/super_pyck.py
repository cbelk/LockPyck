#!/usr/bin/env python

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

import multiprocessing
import datetime
import pyck
import time
import os
from PyckMaster import notdbd

# This file contains the sub-driver for the pycking process and the various functions it
# needs to operate. The dicts:
# cracked => key = hash; value = list of plaintext(s) that hashed to the key hash
#
# Author: Christian Belk

# This function takes the path to the file containing the hashlist, reads the contents into
# the hashlist, and returns it.
def getThoseHashes (hashfile):
    hashlist = []
    if os.path.isfile(hashfile):
        with open(hashfile, 'r') as hashin:
            for hsh in hashin:
                hashlist.append(hsh.strip('\n'))
        hashin.close()
    else:
        print '[-] Super_pyck: %s doesn\'t exist.'
    return hashlist

# This function takes a list of successful cracks (plaintext) and the hashlist. It then adds the hashed
# passwords as the key to the cracked dict and the plaintext into the list (value). Note: list is used
# since collision is possible with random user created passwords (though very, very low probability).
# **Might need to take out the code that removes the hash from hashlist to allow for collision***
def updateCrackedPasses (success, hashlist, cracked):
    for suc in success:
#        print 'updateCrackedPasses: %s  ==>  %s' % (suc[0], suc[1])
        if suc[0] in cracked:
            cracked[suc[0]].append(suc[1])
        else:
            cracked[suc[0]] = [suc[1]]
            c = hashlist.count(suc[0])
            while c > 0:
                hashlist.remove(suc[0])
                c -= 1
    return hashlist

# This function takes the path to the file where the successfuly cracked passwords (or lack thereof in
# the worse case) are stored, and writes the contents of cracked there if cracked is not empty, else
# it prints the failure message.
def crackedWriter (crackedfile, cracked):
#    print cracked
    with open(crackedfile, 'a+') as crackedout:
        crackedout.write('LockPyck run on %s\n' % datetime.datetime.now())
        if cracked:
            for hashd, crack in cracked.iteritems():
                for cc in crack:
                    crackedout.write('[+] Hashed: %s  ||  Password: %s\n' % (hashd, cc))
        else:
            crackedout.write('[-] No hashes were cracked on this run.\n')
        crackedout.write('\n')

# This is the sub-driver for the pycking process. It keeps looping as long as there are hashes to be
# cracked, getting the preterms from the global list and starting a pool of pyck workers to do some cracking.
def main (hashfile, crackedfile, queue, FREAKBASE):
    print '[+] Super_pick: Reading hashes from %s' % hashfile
    hashlist = getThoseHashes(hashfile)
    cracked = {}
    print '[+] Super_pyck: Starting the pycking process ...'
    while hashlist:
        preterms = notdbd.dumpQueue(queue)
        if preterms:
            print '[+] Super_pyck: Got some preterms and starting some pycks ...'
            tupls = []
            for preterm in preterms:
                tupls.append((preterm, hashlist, FREAKBASE))
#            print str(tupls)
            if tupls:
                pool_size = multiprocessing.cpu_count()
                pool = multiprocessing.Pool(processes=pool_size, maxtasksperchild=3,)
                pool_outputs = pool.map(pyck.cutTheKey, tupls)
                pool.close()
                pool.join()
                for success in pool_outputs:
                    if success:
#                        print 'success %s' % str(success)
                        hashlist = updateCrackedPasses(success, hashlist, cracked)
            else:
                print '[+] Super_pyck: Error creating tuples'
                print '[+] Super_pyck: preterm = %s  ||  hashlist = %s' % (str(preterm), str(hashlist))
                break
        else:
            print '[+] Super_pyck: No preterms available right now ...'
            time.sleep(10)
    crackedWriter(crackedfile, cracked)
    return

if __name__ == '__main__':
    main()
