#! /usr/bin/env python

import string
import csv
import os
import shutil
import operator


# This function takes the Seq.freak and the sequence dict as arguments. If Seq.freak 
# already exist, the sequences and freaks in it are merged into the dict. The dict is then
# passed to sortaSeqFreak to be sorted and written.
def freakyUpdate (freaksheet, freaky_dict):
    if os.path.isfile(freaksheet) and os.stat(freaksheet).st_size > 0:
        with open(freaksheet, 'r') as freakin:
            freakyreader = csv.reader(freakin)
            for row in freakyreader:
                if row[0] in freaky_dict:
                    freaky_dict[row[0]] += int(row[1].strip('\n'))
                elif len(row) == 2:
                    freaky_dict[row[0]] = int(row[1].strip('\n'))
        freakin.close()
    sortaSeqFreak(freaksheet, freaky_dict)
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

# This function takes the path to a freak file and a terminal dict. It then iterates
# through the key-value (value is a list here) pairs in the dictionary. It then checks 
# to see if the terminal from each row of the file is in the list. If it is
# then its associated freak from the file is updated with number of times the given
# terminal appears in the list. All occurences of that terminal are then removed from 
# the list. Then all the leftover terminals are written to the file with their freaks.
def updateTerminalFreaks (directFreak, terminal_dict):
    for freakfile, terminalSeq in terminal_dict.iteritems():
        freakf = os.path.join(directFreak, freakfile[:1], freakfile + '.freak')
        termSize = len(terminalSeq)
        if os.path.isfile(freakf):
            with open(freakf, 'r') as freakin, open(freakf + '~', 'w+') as freakout:
                for row in freakin:
                    row = row.strip('\n')
                    dig = len(row) - 1
                    while True:
                        if row[dig].isdigit():
                            dig -= 1
                        elif row[dig] == ',':
                            break
                    freak = int(row[dig + 1:])
                    terminal = row[:dig]
                    if terminal == 'freakycount':
                        freak += termSize
                        freakout.write(terminal + ',' + str(freak) + '\n')
                    elif terminal in terminalSeq:
                        occur = terminalSeq.count(terminal)
                        freak += occur
                        freakout.write(terminal + ',' + str(freak) + '\n')
                        while occur > 0:
                            terminalSeq.remove(terminal)
                            occur -= 1
                    else:
                        freakout.write(terminal + ',' + str(freak) + '\n')
                while len(terminalSeq) > 0:
                    seq = terminalSeq[0]
                    c = terminalSeq.count(seq)
                    freakout.write(seq + ',' + str(c) + '\n')
                    while c > 0:
                        terminalSeq.remove(seq)
                        c -= 1
            freakin.close()
            freakout.close()
            shutil.move(freakf + '~', freakf)
        else:
            with open(freakf, 'w+') as freakout:
                freakout.write('freakycount,' + str(termSize) + '\n')
                while len(terminalSeq) > 0:
                    seq = terminalSeq[0]
                    c = terminalSeq.count(seq)
                    freakout.write(seq + ',' + str(c) + '\n')
                    while c > 0:
                        terminalSeq.remove(seq)
                        c -= 1
            freakout.close()
    return

# This function takes the path to Seq.freak and the sequence dict. It sorts the dict and
# then writes the resulting list to file in the form of csv.
def sortaSeqFreak (freakfile, freaky_dict):
    print '[+] Sorting the freaks in ' + freakfile + '\n'
    with open(freakfile, 'w+') as freakout:
        sorted_freaky = sorted(freaky_dict.items(), key=operator.itemgetter(1), reverse=True)
        for item in sorted_freaky:
            freakout.write(item[0] + ',' + str(item[1]) + '\n')
    freakout.close()
    return

# This function takes the path to a freak file. For each row in the file, the actual 
# comma (as opposed to ones in some S terminals) is found by searching the row in reverse. 
# The row is then split into the terminals and freaks, and a dict is created with the 
# terminals as keys. The dict is then sorted which produces a sorted list of tuples in 
# reverse order. The terminals and freaks from this list are written to the appropriate 
# freak file.
def sortaFreaky (freakfile):
    print '[+] Sorting the freaks in ' + freakfile + '\n'
    if os.path.isfile(freakfile):
        freaky_dict = {}
        with open(freakfile, 'r') as freakin, open(freakfile + '~', 'w+') as freakout:
            for row in freakin:
                row = row.strip('\n')
                dig = len(row) - 1
                while True:
                    if row[dig].isdigit():
                        dig -= 1
                    elif row[dig] == ',':
                        break
                freak = int(row[dig + 1:])
                terminal = row[:dig]
                freaky_dict[terminal] = freak
            sorted_freaky = sorted(freaky_dict.items(), key=operator.itemgetter(1), reverse=True)
            for item in sorted_freaky:
                freakout.write(item[0] + ',' + str(item[1]) + '\n')
        freakin.close()
        freakout.close()
        shutil.move(freakfile + '~', freakfile)
    return
