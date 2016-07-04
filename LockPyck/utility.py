#! /usr/bin/env python

import os

# getThoseHashes takes the path to the file containing the hashlist, reads the contents into
# the hashlist, and returns it.
def getThoseHashes (hashfile):
    hashlist = []
    if os.path.isfile(hashfile):
        with open(hashfile, 'r') as hashin:
            for hsh in hashin:
                hashlist.append(hsh.strip('\n'))
        hashin.close()
    else:
        print '[-] Super_pyck: %s doesn\'t exist.' % hashfile
    return hashlist
