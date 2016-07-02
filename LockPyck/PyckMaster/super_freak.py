#! /usr/bin/env python

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

# This file contains the sub-driver for the freak_roundup and the function used 
# to create the sequence. The dicts and such:
# terminal_dict => key = string (representing non-terminal); value = list of terminals for that non-terminal
# seq_dict      => key = string (representing sequence); value = int (associated freak)
# ndbd_dict     => key = string (representing sequence); value = list version of sequence needed by notdbd
# sequ          => list used to hold individual parts of non-terminals in the sequence. eg ['L', 8, 'D', 3]
#
# Author: Christian Belk

import os
import time
import string
import multiprocessing
import freak_roundup
from itertools import islice

# This function takes a sequence list and a character. If the sequence is empty,
# the character type representation {D igit, L etter, S pecial, W hitespace} is
# added to the list with a count of 1. Otherwise, the previously added char type
# rep is checked to see if it matches the current type. If it does it's count is
# incremented, else it's type rep is added to the list with a count of 1.
def updateSeq (sequ, char):
    if char in string.letters:
        if len(sequ) > 0:
            if sequ[len(sequ) - 2] == 'L':
                sequ[len(sequ) - 1] += 1
            else:
                sequ.append('L')
                sequ.append(1)
        else:
            sequ.append('L')
            sequ.append(1)
    elif char in string.digits:
        if len(sequ) > 0:
            if sequ[len(sequ) - 2] == 'D':
                sequ[len(sequ) - 1] += 1
            else:
                sequ.append('D')
                sequ.append(1)
        else:
            sequ.append('D')
            sequ.append(1)
    elif char in string.punctuation:
        if len(sequ) > 0:
            if sequ[len(sequ) - 2] == 'S':
                sequ[len(sequ) - 1] += 1
            else:
                sequ.append('S')
                sequ.append(1)
        else:
            sequ.append('S')
            sequ.append(1)
    elif char in string.whitespace:
        if len(sequ) > 0:
            if sequ[len(sequ) - 2] == 'W':
                sequ[len(sequ) - 1] += 1
            else:
                sequ.append('W')
                sequ.append(1)
        else:
            sequ.append('W')
            sequ.append(1)
    return sequ

def seqCreator (pswd):
    seq = []
    pswd = pswd.strip('\n')
    for ch in pswd:
        seq = updateSeq(seq, ch)
#    terminal_dict = freak_roundup.updateTerminals(seq, pswd, terminal_dict)
    seqString = ''
    for c in seq:
        seqString += str(c)
    size = len(seq)
    i = 0
    ndbd_seq = []
    while i < size:
        ndbd_seq.append('%s%d' % (seq[i], seq[i+1]))
        i += 2
    return (seqString, ndbd_seq, seq, pswd)

# This function is used to generate batches of passwords from the specified file of size 'chunk'.
# These batches are yielded to be processed as they are created.
def batchGen(passfile, chunk):
    with open(passfile) as pfile:
        while True:
            pswds = list(islice(pfile, chunk))
            if not pswds:
                break
            yield pswds

# This is the sub-driver for the freak_roundup. It creates the sequences from the passwords with
# the help of updateSeq. It then begins calling the functions to update the various freak sheets.
def main(pl, LPYCKBASE, verbose):
    print '[+] Starting the freak roundup ...'
    start = time.time()
    fsheets = os.path.join(LPYCKBASE, 'FreakSheets')
    sqfreak = os.path.join(fsheets, 'Seq.freak')
    ndbdfreak = os.path.join(fsheets, 'NDBD.freak')
    seq_dict = {'freakycount': 0}
    terminal_dict = {}
    ndbd_dict = {}
    group = 1
    for batch in batchGen(pl, 2000000):
        print '[+] Processing batch %s' % group
        print '[+] Starting the pool of workers to analyze the passwords ...'
        batchstart = time.time()
        pool_size = multiprocessing.cpu_count()
        pool = multiprocessing.Pool(processes=pool_size, maxtasksperchild=3,)
        pool_outputs = pool.map(seqCreator, batch)
        pool.close()
        pool.join()
        for tupl in pool_outputs:
            seqString = tupl[0]
            ndbd_seq = tupl[1]
            seq = tupl[2]
            pswd = tupl[3]
            terminal_dict = freak_roundup.updateTerminals(seq, pswd, terminal_dict)
            ndbd_dict[seqString] = ndbd_seq
            if seqString in seq_dict:
                seq_dict[seqString] += 1
            else:
                seq_dict[seqString] = 1
            seq_dict['freakycount'] += 1
        del pool_outputs
        print '[+] Starting the freak update ...'
        if verbose:
            print '[+] Updating NDBD.freak ...'
        freak_roundup.specialFreakyUpdate(ndbdfreak, ndbd_dict, verbose)
        del ndbd_dict
        if verbose:
            print '[+] Updating Seq.freak ...'
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

if __name__ == "__main__":
	main()
