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

# This file contains the function that serves as the workers in the pool for the cracking process.
#
# Author: Christian Belk

import hashlib
import multiprocessing
import os
from PyckMaster import freak_roundup

# This function takes a tuple consisting of a preterminal (represented as a list) and a password
# list (target hashed list). It first determines the non-terminal in the preterminal by searching
# for a mix of letter and digit. It then opens the freaksheet associated with the non-terminal and
# begins plugging them into the preterminal, hashing it, and checking if it's in the password list.
# If it is, the hash and correspomding passwords are returned.
def cutTheKey (tup):
    preterminal = tup[0]
    hashlist = tup[1]
    FREAKBASE = tup[2]
    verbose = tup[3]
#    print hashlist
    nonterm = preterminal[1]
    freaksheet = os.path.join(FREAKBASE, nonterm[0], '%s.freak' % nonterm)
    freaks = freak_roundup.sortaFreaky(freaksheet)
    success = []
    for freak in freaks:
        if freak[0] != 'freakycount':
#            print freak[0]
            passguess = '%s%s' % (preterminal[0], freak[0])
            if verbose:
                print '[+] Pyck: Trying %s' % passguess
            hashed = hashlib.md5()
            hashed.update(passguess)
            hashstring = hashed.hexdigest()
#            print '[+] Pyck: %s =  %s' % (passguess, hashstring)
            if hashstring in hashlist:
                print '[+] Pyck: Success %s ==> %s' % (hashstring, passguess)
                success.append([hashstring, passguess])
    del freaks
#    print success
    return success
