######################### The graveyard of inefficient freaks #########################
#
# This function takes a sequence string argument. If the SeqFreak file contains
# the sequence it's count is incremented by 1, else its added with a count of 1.
#def updateSeqFreak (sequ, count):
#    seqfreakin = os.path.join('..', '..', 'FreakSheets', 'Seq.freak')
#    seqfreakout = seqfreakin + '~'
#    found = False
#    writer = open(seqfreakout, 'a+')
#    if os.path.isfile(seqfreakin) and os.stat(seqfreakin).st_size > 0:
#        with open(seqfreakin, 'r') as seqfreak:
#            reader = csv.reader(seqfreak)
#            for row in reader:
#                if row:
#                    if row[0] == sequ:
#                        found = True
#                        c = int(row[1].strip('\n')) + 1
#                        writer.write(row[0] + ',' + str(c) + '\n')
#                    else:
#                        writer.write(row[0] + ',' + row[1] + '\n')
#        seqfreak.close()
#    if not found:
#        writer.write(sequ + ',1\n')
#    writer.close()
#    shutil.move(seqfreakout, seqfreakin)
#    return count + 1
#
# This function takes a sequence and the associated password. It isolates each part of
# the sequence and generates a file for that particular single non-terminal (eg L6 or D2)
# if one does not already exist. If the file already exist, then it parses it looking
# for a match to the terminal section of the password associated with the single non-
# terminal (eg passowrd = !!freak3 | sequence = S2L5D1 | single non-terminal L5 == freak)
# in which case it increments it's frequency, else it adds it with a frequency of 1.
#def updateTerminalFreaks (sequ, pswd):
#    if len(sequ) > 0:
#        i = 0
#        j = 0 
#        while i < len(sequ):
#            ctype = sequ[i]
#            freakName = os.path.join('..', '..', 'FreakSheets', ctype, ctype + str(sequ[i + 1]) + '.freak')
#            sq = ''
#            h = j		
#            while h < j + sequ[i + 1]:
#                sq += pswd[h]
#                h += 1
#            j += sequ[i + 1]
#            if os.path.isfile(freakName):
#                found = False
#                with open(freakName, 'r') as freakin, open(freakName + '~', 'w+') as freakout:
#                    freakyReader = csv.reader(freakin)
#                    for row in freakyReader:
#                        if len(row) > 1:
#                            if row[0] == sq:
#                                found = True
#                                c = int(row[1].strip('\n')) + 1
#                                freakout.write(row[0] + ',' + str(c) + '\n')
#                            else:
#                                freakout.write(row[0] + ',' + row[1] + '\n')
#                    if not found:
#                        freakout.write(sq + ',' + '1\n')
#                freakin.close()
#                freakout.close()
#                shutil.move(freakName + '~', freakName)
#            else:
#                freaky = open(freakName, 'a+')
#                freaky.write(sq + ',' + '1\n')
#            i += 2
#    return
#
# This function takes the pat to a freakfile and a count as arguments. It then appends
# the count to the end of the file.
#def addFreakinCount (freakfile, count):
#    print '[+] Adding the freakin count to ' + freakfile + '\n'
#    found = False
#    with open(freakfile, 'r') as freakin, open(freakfile + '~', 'a+') as freakout:
#        reader = csv.reader(freakin)
#        i = 0
#        for row in reader:
#            if row[0] == 'count':
#                freakout.write('count,' + str(count) + '\n')
#                found = True
#            else:
#                freakout.write(row[0] + ',' + row[1] + '\n')
#    freakin.close()
#    freakout.close()
#    shutil.move(freakfile + '~', freakfile)
#    if not found:
#        freakyWriter = open(freakfile, 'a+')
#        freakyWriter.write('count,' + str(count) + '\n')
#        freakyWriter.close()
#    return
#
# This function takes the path to a freakfile as an argument. It sums the frequencies in
# the file, and adds the count to the file.
#def createFreakCount (freakfile):
#    print '[+] Counting the freaks in ' + freakfile + '\n'
#    count = 0
#    with open(freakfile, 'r') as freakin:
#        reader = csv.reader(freakin)
#        for row in reader:
#            if row[0] != 'count':
#                if len(row) == 2:
#                    count += int(row[1].strip('\n'))
#    freakin.close()
#    addFreakinCount(freakfile, count)
#    return
#
# This function takes the path to a freakfile as an argument. It then sorts the freakfile
# in descending order of frequencies.
#def sortaFreaky (freakfile):
#    print '[+] Sorting the freaks in ' + freakfile + '\n'
#    cnt = 0
#    at_least_three = False
#    with open(freakfile, 'r') as freakin:
#        for row in freakin:
#            cnt += 1
#            if cnt == 3:
#                at_least_three = True
#                break
#    freakin.close()
#    with open(freakfile, 'r') as freakin, open(freakfile + '~', 'a+') as freakout:
#        reader = csv.reader(freakin)
#        if at_least_three:
#            sortedFreak = sorted(reader, key=lambda ro: int(ro[1]), reverse=True)
#        else:
#            i = 0
#            t0 = []
#            t1 = []
#            for r in reader:
#                if i == 0:
#                    t0 = r
#                else:
#                    t1 = r
#                i += 1
#            sortedFreak = [t1, t0]
#        for row in sortedFreak:
#            freakout.write(row[0] + ',' + row[1] + '\n')
#    freakin.close()
#    freakout.close()
#    shutil.move(freakfile + '~', freakfile)
#    return
# This function takes the FreakSheets directory and the terminal dict. Then for each entr
# in the dict a freakfile name is generated using the key. If the terminals are special
# then control is passed to updateSpecialFreaks to handle the update due to the csv reader
# handling of terminals with commas in them. Else if the file exist the entries are
# updated according to the terminal dict, else the contents of the terminal dict are
# written to file. *works almost the same as updateSpecialFreaks except it uses csv module
#def updateTerminalFreaks (directFreak, terminal_dict):
#    for freakfile, terminalSeq in terminal_dict.iteritems():
#        freakf = os.path.join(directFreak, freakfile[:1], freakfile + '.freak')
#        if freakfile[:1] != 'S':
#            if os.path.isfile(freakf):
#                with open(freakf, 'r') as freakin, open(freakf + '~', 'w+') as freakout:
#                    freakyReader = csv.reader(freakin)
#                    for row in freakyReader:
#                        if len(row) == 2:
#                            if row[0] == 'freakycount':
#                                count = int(row[1].strip('\n')) + len(terminalSeq)
#                                freakout.write(row[0] + ',' + str(count) + '\n')
#                            elif row[0] in terminalSeq:
#                                count = int(row[1].strip('\n')) 
#                                occur = terminalSeq.count(row[0])
#                                count += occur
#                                freakout.write(row[0] + ',' + str(count) + '\n')
#                                while occur > 0:
#                                    terminalSeq.remove(row[0])
#                                    occur -= 1
#                            else:
#                                freakout.write(row[0] + ',' + row[1] + '\n')
#                    while len(terminalSeq) > 0:
#                        seq = terminalSeq[0]
#                        c = terminalSeq.count(seq)
#                        freakout.write(seq + ',' + str(c) + '\n')
#                        while c > 0:
#                            terminalSeq.remove(seq)
#                            c -= 1
#                freakin.close()
#                freakout.close()
#                shutil.move(freakf + '~', freakf)
#            else:
#                with open(freakf, 'w+') as freakout:
#                    freakout.write('freakycount,' + str(len(terminalSeq)) + '\n')
#                    while len(terminalSeq) > 0:
#                        seq = terminalSeq[0]
#                        c = terminalSeq.count(seq)
#                        freakout.write(seq + ',' + str(c) + '\n')
#                        while c > 0:
#                            terminalSeq.remove(seq)
#                            c -= 1
#                freakout.close()
#        else:
#            updateSpecialFreaks(freakf, terminalSeq)
#    return
