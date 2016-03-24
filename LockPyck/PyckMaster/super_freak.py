#! /usr/bin/env python

#########################################################################################
#											#
#    LockPyck -- A Password Cracker Powered By Probabilistic Context free grammars	#
#    Copyright (C) 2016  Christian Belk -- cbelk88@gmail.com				#
#											#
#    This program is free software: you can redistribute it and/or modify		#
#    it under the terms of the GNU General Public License as published by		#
#    the Free Software Foundation, either version 3 of the License, or			#
#    (at your option) any later version.						#
#											#
#    This program is distributed in the hope that it will be useful,			#
#    but WITHOUT ANY WARRANTY; without even the implied warranty of			#
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the			#
#    GNU General Public License for more details.					#
#											#
#    You should have received a copy of the GNU General Public License			#
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.   		#
#											#
#########################################################################################

import os
import time
import string
import freak_roundup
import csv

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
    return

# This is the driver for the freak_roundup. It creates the sequences from the passwords with
# the help of updateSeq. It then begins calling the functions to update the various freak sheets.
def main(pl):
    print '[+] Starting the freak roundup...\n'
    start = time.clock()
    fsheets = os.path.join('..', '..', 'FreakSheets')
    sqfreak = os.path.join(fsheets, 'Seq.freak')
    seq_dict = {'freakycount': 0}
    terminal_dict = {}
    with open(pl) as passlist:
        for pswd in passlist:
            seq = []
            pswd = pswd.strip('\n')
            for ch in pswd:
                updateSeq(seq, ch)
            terminal_dict = freak_roundup.updateTerminals(seq, pswd, terminal_dict)
            seqString = ''
            for c in seq:
                seqString += str(c)
            if seqString in seq_dict:
                seq_dict[seqString] += 1
            else:
                seq_dict[seqString] = 1
            seq_dict['freakycount'] += 1
    passlist.close()
    freak_roundup.freakyUpdate(sqfreak, seq_dict)
    freak_roundup.updateTerminalFreaks(fsheets, terminal_dict)
    types = ['D','L','W']
#    for t in types:
#        for freak in os.listdir(os.path.join(fsheets, t)):
#            if freak.endswith('.freak'):
#                freak_roundup.sortaFreaky(os.path.join(fsheets, t, freak))
#    for freak in os.listdir(os.path.join(fsheets, 'S')):
#        if freak.endswith('.freak'):
#            freak_roundup.sortaFreaky(os.path.join(fsheets, 'S', freak))
    runtime = time.clock() - start
    if runtime > 60:
        print '[+] Freak roundup finished in ' + str(runtime / 60) + ' minute(s)'
    else:
        print '[+] Freak roundup finished in ' + str(runtime) + ' seconds\n'
    return

if __name__ == "__main__":
	main()
