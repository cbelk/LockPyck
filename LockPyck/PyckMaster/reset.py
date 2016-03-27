#!/usr/bin/env python

import os

def freakyReset (FREAKBASE):
    decision = raw_input('[+] Are you sure you want to delete the freaksheets? (y/n) ')
    if decision.lower() == 'y':
        try:
            os.remove(os.path.join(FREAKBASE, 'Seq.freak'))
        except:
            pass
        termDirects = ['L','S','D','W']
        for direct in termDirects:
            for freak in os.listdir(os.path.join(FREAKBASE, direct)):
                if '.freak' in freak:
                    os.remove(os.path.join(FREAKBASE, direct, freak))
        print '[+] Freaksheets deleted'
    elif decision.lower() != 'n':
        print '[-] Invalid option'
        print '[-] No freaksheets are getting deleted'
    else:
        print '[+] No freaksheets deleted'
    return
