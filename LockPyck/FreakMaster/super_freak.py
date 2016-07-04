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

# This file contains the sub-driver for the freak_roundup.
# The data structures:
# terminal_dict => key = string (representing non-terminal); value = list of terminals for that non-terminal
# seq_dict      => key = string (representing sequence); value = int (associated freak)
# ndbd_dict     => key = string (representing sequence); value = list version of sequence
#
# Author: Christian Belk

import freak_roundup
import multiprocessing
import os
import seq_help
import time
import futility

# This is the sub-driver for the freak_roundup. It creates the sequences from the passwords with
# the help of updateSeq. It then begins calling the functions to update the various freak sheets.
def drive(pl, LPYCKBASE, verbose):
    print '[+] Starting the freak roundup ...'
    start = time.time()
    fsheets = os.path.join(LPYCKBASE, 'FreakSheets')
    sqfreak = os.path.join(fsheets, 'Seq.freak')
    ndbdfreak = os.path.join(fsheets, 'NDBD.freak')
    seq_dict = {'freakyc0unt': 0}
    terminal_dict = {}
    ndbd_dict = {}
    group = 1
    for batch in futility.batchGen(pl, 2000000):
        print '[+] Processing batch %s' % group
        print '[+] Starting the pool of workers to analyze the passwords ...'
        batchstart = time.time()
        pool_size = multiprocessing.cpu_count()
        pool = multiprocessing.Pool(processes=pool_size, maxtasksperchild=3,)
        pool_outputs = pool.map(seq_help.seqCreator, batch)
        pool.close()
        pool.join()
        for tupl in pool_outputs:
            seqString = tupl[0]
            seq = tupl[1]
            pswd = tupl[2]
            terminal_dict = freak_roundup.updateTerminals(seq, pswd, terminal_dict)
            ndbd_dict[seqString] = seq
            if seqString in seq_dict:
                seq_dict[seqString] += 1
            else:
                seq_dict[seqString] = 1
            seq_dict['freakyc0unt'] += 1
        del pool_outputs
        print '[+] Starting the freak update ...'
        freak_roundup.freakyUpdate(ndbdfreak, ndbd_dict, verbose)
        del ndbd_dict
        freak_roundup.freakyUpdate(sqfreak, seq_dict, verbose)
        del seq_dict
        if verbose:
            print '[+] Updating the terminal freaks ...'
        freak_roundup.updateTerminalFreaks(fsheets, terminal_dict, verbose)
        rtime = time.time() - batchstart
        if rtime > 60:
            print '[+] Batch %d roundup finished in %d minute(s)' % (group, rtime / 60)
        else:
            print '[+] Batch %d roundup finished in %d seconds' % (group, rtime)
        group += 1
    runtime = time.time() - start
    if runtime > 60:
        print '[+] Freak roundup finished in ' + str(runtime / 60) + ' minute(s)'
    else:
        print '[+] Freak roundup finished in ' + str(runtime) + ' seconds'
    return
