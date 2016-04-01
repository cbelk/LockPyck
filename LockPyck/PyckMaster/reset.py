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

import os

def freakyReset (FREAKBASE):
    decision = raw_input('[+] Are you sure you want to delete the freaksheets? (y/n) ')
    if decision.lower() == 'y':
        try:
            os.remove(os.path.join(FREAKBASE, 'Seq.freak'))
            os.remove(os.path.join(FREAKBASE, 'NDBD.freak'))
        except:
            pass
        termDirects = ['L','S','D','W']
        for direct in termDirects:
            for freak in os.listdir(os.path.join(FREAKBASE, direct)):
                if '.freak' in freak:
                    os.remove(os.path.join(FREAKBASE, direct, freak))
        print '[+] Freaksheets deleted'
    elif decision.lower() != 'n':
        print '[-] Invalid option'
        print '[-] No freaksheets are getting deleted'
    else:
        print '[+] No freaksheets deleted'
    return
