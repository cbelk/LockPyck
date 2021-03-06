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

# This file contains the function that serves as the workers in the pool for the cracking process.
#
# Author: Christian Belk

import hashlib
import os
from FreakMaster import freak_roundup

# cutTheKey is used to perform the actual cracking. After determining the non-terminal, it
# retrieves the sorted content of the associated freaksheet and begins plugging them into
# the preterminal to form a password guess which is then hashed and compared to the hashlist.
# Successful cracks are added to a list which is returned.
def cutTheKey(tup):
    preterminal = tup[0]
    hashlist = tup[1]
    FREAKBASE = tup[2]
    verbose = tup[3]
    if len(preterminal) == 1:
        nonterm = preterminal[0]
    else:
        nonterm = preterminal[1]
    freaksheet = os.path.join(FREAKBASE, nonterm[0], '%s.freak' % nonterm)
    freaks = freak_roundup.sortaFreaky(freaksheet)
    success = []
    for freak in freaks:
        if freak[0] != 'freakyc0unt':
            if len(preterminal) == 1:
                passguess = freak[0]
            else:
                passguess = '%s%s' % (preterminal[0], freak[0])
            if verbose:
                print '[+] Pyck: Trying %s' % passguess
            hashed = hashlib.md5()
            hashed.update(passguess)
            hashstring = hashed.hexdigest()
            if hashstring in hashlist:
                success.append([hashstring, passguess])
    del freaks
    return success
