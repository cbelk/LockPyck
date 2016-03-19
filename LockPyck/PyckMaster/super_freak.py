#! /usr/bin/env python

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
    if os.path.isfile(sqfreak) and os.stat(sqfreak).st_size > 0:
        with open(sqfreak, 'r') as sqf:
            reader = csv.reader(sqf)
            for row in reader:
                if row[0] == 'count':
                    count = int(row[1].strip('\n'))
                    break
        sqf.close()
    else:
        count = 0
    with open(pl) as passlist:
        for pswd in passlist:
            seq = []
            pswd = pswd.strip('\n')
            for ch in pswd:
                updateSeq(seq, ch)
            freak_roundup.updateTerminalFreaks(seq, pswd)
            seqString = ''
            for c in seq:
                seqString += str(c)
            count = freak_roundup.updateSeqFreak(seqString, count)
    freak_roundup.addFreakinCount(sqfreak, count)
    types = ['D','L','S','W']
    for t in types:
        for freak in os.listdir(os.path.join(fsheets, t)):
            if freak.endswith('.freak'):
                freak_roundup.createFreakCount(os.path.join(fsheets, t, freak))
                freak_roundup.sortaFreaky(os.path.join(fsheets, t, freak))
    freak_roundup.sortaFreaky(sqfreak)
    print '[+] Freak roundup finished in ' + str(time.clock() - start) + 'seconds\n'
    return

if __name__ == "__main__":
	main()
