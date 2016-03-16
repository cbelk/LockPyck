#! /usr/bin/env python

import string
import csv
import os
import shutil
import operator

lp = '***/LockPyck/'  #replace *** with path to LockPyck

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

# This function takes a sequence string argument. If the SeqFreak file contains
# the sequence it's count is incremented by 1, else its added with a count of 1.
def updateSeqFreak (sequ):
    seqfreakin = lp + 'FreakSheets/Seq.freak'
    seqfreakout = seqfreakin + '~'
    found = False
    writer = open(seqfreakout, 'a+')
    if os.path.isfile(seqfreakin) and os.stat(seqfreakin).st_size > 0:
        with open(seqfreakin, 'r') as seqfreak:
            reader = csv.reader(seqfreak)
            for row in reader:
                if row:
                    if row[0] == sequ:
                        found = True
                        c = row[1].strip('\n')
                        count = int(c) + 1
                        row[1] = str(count) + '\n'
                        writer.write(row[0] + ',' + row[1])
                    else:
                        a = row[1].strip('\n')
                        writer.write(row[0] + ',' + a + '\n')
        seqfreak.close()
    if not found:
        writer.write(sequ + ',1\n')
    writer.close()
    shutil.move(seqfreakout, seqfreakin)
    return

# This function takes the path to a freakfile as an argument. It sums the frequencies in
# the file, and adds the count to the file.
def createFreakCount (freakfile):
    print '[+] Counting the freaks in ' + freakfile + '\n'
    count = 0
    with open(freakfile, 'r') as freakin:
        reader = csv.reader(freakin)
        for row in reader:
            if len(row) == 2:
                count += int(row[1].strip('\n'))
    freakin.close()
    with open(freakfile, 'r') as freakin, open(freakfile + '~', 'a+') as freakout:              #Just add count to end since sortaFreaky
        freakout.write('count,' + str(count) + '\n')                                            #will move to top
        for line in freakin:
            freakout.write(line)
    freakin.close()
    freakout.close()
    shutil.move(freakfile + '~', freakfile)
    return

# This function takes the path to a freakfile as an argument. It then sorts the freakfile
# in descending order of frequencies.
def sortaFreaky (freakfile):
    print '[+] Sorting the freaks in ' + freakfile + '\n'
    with open(freakfile, 'r') as freakin, open(freakfile + '~', 'a+') as freakout:
        reader = csv.reader(freakin)
        sortedFreak = sorted(reader, key=lambda ro: int(ro[1]), reverse=True)
        for row in sortedFreak:
#            print row[0] + ',' + row[1] + '\n'
            freakout.write(row[0] + ',' + row[1] + '\n')
    freakin.close()
    freakout.close()
    shutil.move(freakfile + '~', freakfile)

print '[+] Starting the freak roundup...\n'

pl = '***'  #replace *** with path to password list
with open(pl) as passlist:
    for pswd in passlist:
        seq = []
        pswd = pswd.strip('\n')
        for ch in pswd:
            updateSeq(seq, ch)
        seqString = ''
        for c in seq:
            seqString += str(c)
        updateSeqFreak(seqString)
createFreakCount(lp + 'FreakSheets/Seq.freak')
sortaFreaky(lp + 'FreakSheets/Seq.freak')
