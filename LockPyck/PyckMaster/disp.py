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

# This file contains the functions needed to display the various freaksheets.
#
# Author: Christian Belk

import os
import pickle
import freak_roundup

# This function takes the path to a freaksheet. It then unpickles it and displays it's contents
# if it exists.
def showTheFreak (freaksheet):
    if os.path.isfile(freaksheet):
        freaks = freak_roundup.sortaFreaky(freaksheet)
        print '[+] UnPickled Contents of %s:' % freaksheet
        for freak in freaks:
            print '%s, %d' % (freak[0], freak[1])
        del freaks
    else:
        print '[-] The specified file doesn\'t exist'

# This function takes the path to the NDBD.freak, unpickles it, and displays it's contents if
# it exist.
def showTheSpecialFreak (freaksheet):
    if os.path.isfile(freaksheet):
        with open(freaksheet, 'rb') as freakin:
            stale_pickle = pickle.load(freakin)
        freakin.close()
        print '[+] UnPickled Contents of %s:' % freaksheet
        for seqstring, seqlist in stale_pickle.iteritems():
            print '%s ==> %s' % (seqstring, str(seqlist))
        del stale_pickle
    else:
        print '[-] The specified file doesn\'t exist'
