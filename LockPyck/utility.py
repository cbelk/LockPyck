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
import time
try:
    import psutil
except:
    print '[-] The psutil module is required.\n[-] You can use a package manager to install it (e.g. pip install psutil).'
    sys.exit()

# corrupt is used to check if the password file that was passed to the leaning phase has
# been analyzed before, returning true if it has and false otherwise.
def corrupt(passfile, learnedlog):
    if os.path.exists(learnedlog):
        with open(learnedlog, 'r') as learnin:
            for row in learnin:
                if passfile in row:
                    return True
        learnin.close()
    return False

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

# freakyReset takes the path to the FreakSheets directory and then deletes all of the 
# freaksheets there and in all the terminal subdirectories if the user verifies they want
# them deleted.
def freakyReset(FREAKBASE, LOGBASE):
    decision = raw_input('[!] Are you sure you want to delete the freaksheets and logs? (y/n) ')
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
        for log in os.listdir(LOGBASE):
            if '.log' in log:
                os.remove(os.path.join(LOGBASE, log))
        print '[+] Logs deleted'
    elif decision.lower() != 'n':
        print '[-] Invalid option'
        print '[-] No freaksheets are getting deleted'
    else:
        print '[+] No freaksheets deleted'
    return

# getThoseHashes takes the path to the file containing the hashlist, reads the contents into
# the hashlist, and returns it.
def getThoseHashes(hashfile):
    hashlist = []
    if os.path.isfile(hashfile):
        with open(hashfile, 'r') as hashin:
            for hsh in hashin:
                hashlist.append(hsh.strip('\n'))
        hashin.close()
    else:
        print '[-] Super_pyck: %s doesn\'t exist.' % hashfile
    return hashlist

# log takes the path to a logfile and a message and writes the message to file.
def log(logfile, message):
    with open(logfile, 'a+') as logout:
        logout.write(message)
    logout.close()
    return
