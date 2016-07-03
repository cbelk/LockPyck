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

# This file contains the utility functions used in PyckTool.
#
# Author: Christian Belk

import datetime
import os

# crackedWriter takes the path to the file where the successfuly cracked passwords (or lack thereof in
# the worse case) are stored, and writes the contents of cracked there if cracked is not empty, else
# it prints the failure message.
def crackedWriter (crackedfile, cracked):
    with open(crackedfile, 'a+') as crackedout:
        crackedout.write('LockPyck run on %s\n' % datetime.datetime.now())
        if cracked:
            for hashd, crack in cracked.iteritems():
                for cc in crack:
                    crackedout.write('[+] Hashed: %s  ||  Password: %s\n' % (hashd, cc))
        else:
            crackedout.write('[-] No hashes were cracked on this run.\n')
        crackedout.write('\n')
    return

# getThoseHashes takes the path to the file containing the hashlist, reads the contents into
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
