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

# This file contains the various functions for creating, storing, and sorting the freaks.
# The data structures:
# freaky_dict   => key = string (representing sequence or terminal); value = int (the freak)
# ndbd_dict     => key = string (representing sequence); value = list version of the sequence
# terminal_dict => key = string (representing non-terminal); value = list of terminals for that non-terminal
# stale_pickle  => the dict returned from un-pickling a given freaksheet
#
# Author: Christian Belk

import multiprocessing
import os
import operator
import string
from collections import Counter
try:
    import cPickle as pickle
except:
    import pickle

# freakyCreator is used to create the freaky_dict from the given list of terminals
# that belong to the given non-terminal. This is then passed to freakyUpdate to be
# merged and pickled.
def freakyCreator (freaky_tuple):
    freakfile = freaky_tuple[0]
    terminalSeq = freaky_tuple[1]
    directFreak = freaky_tuple[2]
    verbose = freaky_tuple[3]
    freakf = os.path.join(directFreak, freakfile[:1], freakfile + '.freak')
    freaky_dict = {'freakyc0unt': len(terminalSeq)}
    while len(terminalSeq) > 0:
        seq = terminalSeq[0]
        if seq in freaky_dict:
            freaky_dict[seq] += 1
        else:
            freaky_dict[seq] = 1
        terminalSeq.remove(seq)
    freakyUpdate(freakf, freaky_dict, verbose)
    return

# freakyUpdate is used to update the freaksheets. If the freaksheet exists and its
# NDBD's, the contents are merged with freaky_dict and pickled to the freaksheet. If
# it exists but is not the NDBD.freak, then the contents are merged (summing the 
# frequencies of duplicates), and pickled to the freaksheet. Else if no freaksheet
# exists, freaky_dict is just pickled out to file.
def freakyUpdate (freaksheet, freaky_dict, verbose):
    if verbose:
        print '[+] FreakyUpdate: Updating %s' % freaksheet
    if os.path.isfile(freaksheet) and os.stat(freaksheet).st_size > 0:
        with open(freaksheet, 'rb') as freakin:
            stale_pickle = pickle.load(freakin)
        freakin.close()
        if 'NDBD.freak' in freaksheet:
            freaky_dict = dict(stale_pickle.items() + freaky_dict.items())
        else:
            freaky_dict = dict(Counter(stale_pickle) + Counter(freaky_dict))
    with open(freaksheet, 'wb') as freakout:
        pickle.dump(freaky_dict, freakout)
    freakout.close()
    return

# getMeThatFreak takes the path to a freaksheet. It un-pickles it and returns it if it exist.
def getMeThatFreak (freaksheet):
    if os.path.isfile(freaksheet):
        with open(freaksheet, 'rb') as freakin:
            stale_pickle = pickle.load(freakin)
        freakin.close()
        return stale_pickle
    return

# sortaFreaky is used to return the sorted contents of the given freaksheet.
def sortaFreaky (freaksheet):
    if os.path.isfile(freaksheet):
        sort = sorted(getMeThatFreak(freaksheet).items(), key=operator.itemgetter(1), reverse=True)
        return sort
    return

# updateTerminalFreaks creates a list of jobs (tuples) which it passes to a pool 
# of workers running the freakyCreator function.
def updateTerminalFreaks (directFreak, terminal_dict, verbose):
    freaky_jobs = []
    pool_size = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=pool_size, maxtasksperchild=3,)
    for freakfile, terminalSeq in terminal_dict.iteritems():
        freaky_jobs.append((freakfile, terminalSeq, directFreak, verbose))
    pool.map(freakyCreator, freaky_jobs)
    pool.close()
    pool.join()
    return

# updateTerminals takes a sequence, its corresponding password, and the terminal dict.
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
