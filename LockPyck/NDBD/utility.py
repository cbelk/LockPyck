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

# This file contains the utilities used by notdbd, cartersianPreterms, as well as outside modules.
#
# Author: Christian Belk

import time
try:
    import psutil
except:
    print '[-] The psutil module is required.\n[-] You can use a package manager to install it (e.g. pip install psutil).'
    sys.exit()

# courtesyCheck is used to throttle the program if memory usage gets too high.
def courtesyCheck(THRESHOLD):
    ram = psutil.virtual_memory()
    swp = psutil.swap_memory()
    while ram.percent > THRESHOLD:
        if swp.total == 0:
            print '[!] Notdbd: Taking a break since memory usage is high ...'
            time.sleep(30)
        elif swp.percent > THRESHOLD:
            print '[!] Notdbd: Taking a break since memory usage is high ...'
            time.sleep(30)
        else:
            break
        ram = psutil.virtual_memory()
        swp = psutil.swap_memory()
    return

# dumpQueue empties the contents of the queue into a list which is then returned.
def dumpQueue (queue):
    preterms = []
    while not queue.empty():
        preterms.append(queue.get())
    return preterms
