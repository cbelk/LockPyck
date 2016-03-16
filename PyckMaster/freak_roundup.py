#! /usr/bin/env python

import string
import csv
import os
import shutil

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

def updateSeqFreak (sequ):
    seqfreakfile = '***/LockPyck/FreakSheets/Seq.freak' #replace *** with path to LockPyck
    seqfreakwrite = seqfreakfile + '~'
    found = False
    writer = open(seqfreakwrite, 'a+')
    if os.stat(seqfreakfile).st_size > 0:
        with open(seqfreakfile, 'r') as seqfreak:
            reader = csv.reader(seqfreak)
            for row in reader:
                if row:
                    if row[0] == sequ:
                        found = True
                        c = row[1].strip('\n')
                        count = int(c) + 1
                        row[1] = str(count) + '\n'
                        writer.write(row[0] + ',' + str(row[1]) + '\n')
                    else:
                        writer.write(row[0] + ',' + str(row[1]) + '\n')
        seqfreak.close()
    if not found:
        writer.write(sequ + ',1\n')
    writer.close()
    shutil.move(seqfreakwrite, seqfreakfile)
    return

def createFreakCount (freakfile):
    count = 0
    with open(freakfile, 'r') as freakin:
        reader = csv.reader(freakin)
        for row in reader:
            print row
            if len(row) == 2:
                count += int(row[1].strip('\n'))
    freakin.close()
    with open(freakfile, 'r') as freakin, open (freakfile + '~', 'a+') as freakout:
        freakout.write('count,' + str(count) + '\n')
        for line in freakin:
            freakout.write(line)
    freakin.close()
    freakout.close()
    shutil.move(freakfile + '~', freakfile)
    return

with open('***') as passlist:  #replace *** with path to password list
    for pswd in passlist:
        seq = []
        pswd = pswd.strip('\n')
        for ch in pswd:
            updateSeq(seq, ch)
        seqString = ''
        for c in seq:
            seqString += str(c)
        updateSeqFreak(seqString)
createFreakCount('***/LockPyck/FreakSheets/Seq.freak')  #replace *** with path to LockPyck
