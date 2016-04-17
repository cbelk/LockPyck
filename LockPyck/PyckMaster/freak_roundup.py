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

# This file contains the various functions for creating, storing, and sorting the freaks. The dicts:
# freaky_dict   => key = string (representing sequence or terminal); value = int (the freak)
# ndbd_dict     => key = string (representing sequence); value = list version of sequence needed by notdbd
# terminal_dict => key = string (representing non-terminal); value = list of terminals for that non-terminal
# stale_pickle  => the dict returned from un-pickling a given freaksheet
#
# Author: Christian Belk

import os
import operator
import string
import multiprocessing
from collections import Counter
try:
    import cPickle as pickle
except:
    import pickle

# This function takes the path to a freaksheet and a dict. If the file exists,
# the contents are un-pickled and loaded into a dict. The two dicts are merged 
# adding the freaks (value) for each sequence or terminal (key). The resulting dict
# is pickled and dumped back to file. If the file doesn't exist the dict is pickled
# and dumped to file.
def freakyUpdate (freaksheet, freaky_dict):
    print '[+] FreakyUpdate: Updating %s' % freaksheet
    if os.path.isfile(freaksheet) and os.stat(freaksheet).st_size > 0:
        with open(freaksheet, 'rb') as freakin:
            stale_pickle = pickle.load(freakin)
        freakin.close()
        out_dict = dict(Counter(stale_pickle) + Counter(freaky_dict))
        with open(freaksheet, 'wb') as freakout:
            pickle.dump(out_dict, freakout)
        freakout.close()
    else:
        with open(freaksheet, 'wb') as freakout:
            pickle.dump(freaky_dict, freakout)
        freakout.close()
    return

# This function takes the path to the NDBD.freak sheet and the ndbd_dict. If the
# file exists, its contents are un-pickled, and merged with ndbd_dict. It's then
# pickled back to file. Else, it's just pickled to file.
def specialFreakyUpdate (freaksheet, ndbd_dict):
    print '[+] FreakyUpdate: Updating %s' % freaksheet
    if os.path.isfile(freaksheet) and os.stat(freaksheet).st_size > 0:
        with open(freaksheet, 'rb') as freakin:
            stale_pickle = pickle.load(freakin)
        freakin.close()
        out_dict = dict(stale_pickle.items() + ndbd_dict.items())
        with open(freaksheet, 'wb') as freakout:
            pickle.dump(out_dict, freakout)
        freakout.close()
    else:
        with open(freaksheet, 'wb') as freakout:
            pickle.dump(ndbd_dict, freakout)
        freakout.close()
    return   

# This function takes the path to the FreakSheets directory and a terminal dict.
# It then creates a list of jobs (tuples) which it passes to a pool of workers running 
# the freakyCreator function.
def updateTerminalFreaks (directFreak, terminal_dict):
    freaky_jobs = []
    pool_size = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=pool_size, maxtasksperchild=3,)
    for freakfile, terminalSeq in terminal_dict.iteritems():
        freaky_jobs.append((freakfile, terminalSeq, directFreak))
    pool.map(freakyCreator, freaky_jobs)
    pool.close()
    pool.join()
    return

# This function takes a tuple consisting of a non-terminal, a list of terminals belonging to 
# that non-terminal, and the path to the FreakSheets directory. It then creates a freaky_dict
# using the terminal list and the path to the freaksheet using the non-terminal. These are 
# then passed to freakyUpdate to be pickled.
def freakyCreator (freaky_tuple):
    freakfile = freaky_tuple[0]
#    print '[!] freakyCreator: working on %s' % freakfile
    terminalSeq = freaky_tuple[1]
    directFreak = freaky_tuple[2]
    freakf = os.path.join(directFreak, freakfile[:1], freakfile + '.freak')
    freaky_dict = {'freakycount': len(terminalSeq)}
    while len(terminalSeq) > 0:
        seq = terminalSeq[0]
        if seq in freaky_dict:
            freaky_dict[seq] += 1
        else:
            freaky_dict[seq] = 1
        terminalSeq.remove(seq)
#        print '[!] freakyCreator: processing sequence: %s' % seq
#        c = terminalSeq.count(seq)
#        freaky_dict[seq] = c
#        freaky_dict['freakycount'] += c
#        while c > 0:
#            terminalSeq.remove(seq)
#            c -= 1
    freakyUpdate(freakf, freaky_dict,)
    return

# This function takes a sequence, its corresponding password, and the terminal dict.
# Then for each single non-terminal in the sequence, it isolates it's corresponding part
# from the password, and checks to see if that non-terminal exist in the dict, appending
# the sequence if it does, else adding it with a list (value) containing the sequence.
def updateTerminals (sequ, pswd, terminal_dict):
    if len(sequ) > 0:
        i = 0
        j = 0
        while i < len(sequ):
            ctype = sequ[i]
            sq = ''
            h = j
            while h < j + sequ[i + 1]:
                sq += pswd[h]
                h += 1
            j += sequ[i + 1]
            freakf = ctype + str(sequ[i + 1])
            if freakf in terminal_dict:
                terminal_dict[freakf].append(sq)
            else:
                terminal_dict[freakf] = [sq]
            i += 2
    return terminal_dict

# This function takes the path to a freaksheet. It un-pickles it, and passes it to sorted,
# which returns a sorted list of tuples.
def sortaFreaky (freaksheet):
    if os.path.isfile(freaksheet):
        with open(freaksheet, 'rb') as freakin:
            stale_pickle = pickle.load(freakin)
        freakin.close()
        sort = sorted(stale_pickle.items(), key=operator.itemgetter(1), reverse=True)
        del stale_pickle
        return sort
    return

# This funtion takes the path to a freaksheet. It un-pickles it and returns it if it exist.
def getMeThatFreak (freaksheet):
    if os.path.isfile(freaksheet):
        with open(freaksheet, 'rb') as freakin:
            stale_pickle = pickle.load(freakin)
        freakin.close()
        return stale_pickle
    return
