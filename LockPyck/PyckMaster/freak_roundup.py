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

import os
import operator
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

# This function takes the path to the FreakSheets directory and a terminal dict.
# Then for each entry in the dict, it uses the key to create the path to its freaksheet
# and the list value is turned into a freaky dict. These are both passed to freakyUpdate
# for pickling.
def updateTerminalFreaks (directFreak, terminal_dict):
    freaky_jobs = []
    pool_size = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=pool_size, maxtasksperchild=3,)
    for freakfile, terminalSeq in terminal_dict.iteritems():
        freaky_jobs.append((freakfile, terminalSeq, directFreak))
    pool_outputs = pool.map(freakyCreator, freaky_jobs)
    pool.close()
    pool.join()
#    for outp in pool_outputs:
#        freakyUpdates(outp)
#        freakf = os.path.join(directFreak, freakfile[:1], freakfile + '.freak')
#        freaky_dict = {'freakycount': 0}
#        while len(terminalSeq) > 0:
#            seq = terminalSeq[0]
#            c = terminalSeq.count(seq)
#            freaky_dict[seq] = c
#            freaky_dict['freakycount'] += c
#            while c > 0:
#                terminalSeq.remove(seq)
#                c -= 1
#        proc = multiprocessing.Process(target=freakyUpdate, args=(freakf, freaky_dict))
#        freaky_jobs.append(proc)
#        proc.start()
#        tupls.append((freakf, freaky_dict,))
#    pool_size = multiprocessing.cpu_count()
#    pool = multiprocessing.Pool(processes=pool_size, initializer=start_proc, maxtasksperchild=3,)
#    print tupls
#    pool_outputs = pool.map(freakyUpdates, tupls)
#    pool.close()
#    pool.join()
#        freakyUpdate(freakf, freaky_dict)
    return

def freakyCreator (freaky_tuple):
    freakfile = freaky_tuple[0]
    terminalSeq = freaky_tuple[1]
    directFreak = freaky_tuple[2]
    freakf = os.path.join(directFreak, freakfile[:1], freakfile + '.freak')
    freaky_dict = {'freakycount': 0}
    while len(terminalSeq) > 0:
        seq = terminalSeq[0]
        c = terminalSeq.count(seq)
        freaky_dict[seq] = c
        freaky_dict['freakycount'] += c
        while c > 0:
            terminalSeq.remove(seq)
            c -= 1
    freakyUpdate(freakf, freaky_dict,)
    return

# This function takes a sequence, its corresponding password, and the terminal dict.
# Then for each single non-terminal in the sequence, it isolates it's corresponding part
# from the password, and checks to see if that terminal exist in the dict, updating it's
# freak if it does, else adding it with a freak of 1. 
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
        return sorted(stale_pickle.items(), key=operator.itemgetter(1), reverse=True)
    return
