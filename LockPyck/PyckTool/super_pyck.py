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
import pyck
from PyckMaster import notdbd

def getThoseHashes (hashfile):
    hashlist = []
    with open(hashfile, 'r') as hashin:
        for hsh in hashin:
            hashlist.append(hsh)
    hashin.close()
    return hashlist

cracked = {}
def updateCrackedPasses (success, hashlist):
    if success[0] in cracked:
        cracked[success[0]].append(success[1])
    else:
        cracked[success[0]] = success[1]
        c = hashlist.count(success[0])
        while c > 0:
            hashlist.remove(success[0])
            c -= 1
    return hashlist

def crackedWriter (crackedfile):
    with open(crackedfile, 'a+') as crackedout:
        if cracked:
            for hashd, crack in cracked:
                for cc in crack:
                    crackedout.write('[+] Hashed: %s  ||  Password: %s' % (hashd, cc))
        else:
            crackedout.write('[-] No hashes were cracked on this run.')
        
def main (hashfile, crackedfile):
    hashlist = getThoseHashes(hashfile)
    while hashlist:
        preterms = notdbd.emptyGlobal()
        tupls = []
        for preterm in preterms:
            tupls.append((preterm, hashlist))
        pool_size = multiprocessing.cpu_count()
        pool = multiprocessing.Pool(processes=pool_size, maxtasksperchild=3,)
        pool_outputs = pool.map(pyck.cutTheKey, tupls)
        pool.close()
        pool.join()
        for success in pool_outputs:
            if success:
                hashlist = updateCrackedPasses(success)
    crackedWriter(crackedfile)
    return

if __name__ == '__main__':
    main()
