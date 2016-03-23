#!/usr/bin/env python

import hashlib
import os

# This function takes a tuple consisting of a preterminal (represented as a list) and a password
# list (target hashed list). It first determines the non-terminal in the preterminal by searching
# for a mix of letter and digit. It then opens the freaksheet associated with the non-terminal and
# begins plugging them into the preterminal, hashing it, and checking if it's in the password list.
# If it is, the hash and correspomding passwords are returned.
def cutTheKey (tup):
    preterminal = tup[0]
    passlist = tup[1]
    nonterm = ''
    for term in preterminal:
        if len(term) >= 2 and term[0].isalpha() and term[1].isdigit():
            nonterm = term
    freaksheet = os.path.join('..', '..', 'FreakSheets', nonterm[0], '%s.freak' % nonterm)
    with open(freaksheet) as freakin:
        for row in freakin:
            row = row.strip('\n')
            dig = len(row) - 1
            while True:
                if row[dig].isdigit():
                    dig -= 1
                elif row[dig] == ',':
                    break
            terminal = row[:dig]
            if terminal != 'freakycount':
                password = ''
                for term in preterminal:
                    if term == nonterm:
                        password += terminal
                    else:
                        password += term
                hashed = hashlib.md5()
                hashed.update(password)
                hashstring = hashed.hexdigest()
#                print password + '\n'
#                print hashstring
                if hashstring in passlist:
                    print 'found %s' % password
                    print hashstring
                    return [hashstring, password]
    freakin.close()
    return
