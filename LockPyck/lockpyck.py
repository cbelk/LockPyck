#!/usr/bin/env python

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

# This file contains the main driver for LockPyck. The help menu can be accessed by either 
# the -h option or just calling lockpyck without any arguments.
#
# Author: Christian Belk

import argparse
import multiprocessing
import os
import sys
import utility as util
from FreakMaster import super_freak
from FreakMaster import utility as futil
from NDBD import notdbd
from PyckTool import super_pyck
from PyckTool import daemon_writer

# This is the main driver for LockPyck. It simply takes the command line arguments and calls
# the appropriate method(s) and/or sub-driver(s).
def main ():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--psswdHash', help='specify the absolute path to the file containing the hash(es) to be cracked (one hash per line)')
    parser.add_argument('-l', '--learn', help='specify the absolute path to a file containing plain text passwords to learn from (one password per line)')
    parser.add_argument('-d', '--display', help='specify the freaksheet to display (eg Seq or L6 if avalaible)')
    parser.add_argument('-v', '--verbose', action='store_true', help='verbose mode')
    parser.add_argument('-r', '--remove', action='store_true', help='remove all freaksheets')
    args = parser.parse_args()
    DRIVER = os.path.abspath(__file__)
    PYCKBASE = os.path.dirname(DRIVER)
    LPYCKBASE = PYCKBASE[:-8]
    FREAKBASE = os.path.join(LPYCKBASE, 'FreakSheets')
    LOGBASE = os.path.join(LPYCKBASE, 'log')
    LEARNED = os.path.join(LOGBASE, 'learned.log')
    CRACKEDLIST = os.path.join(LPYCKBASE, 'cracked.freak')
    POISON_PILL = 'kcyPkcoL'
    PILL_COUNT = multiprocessing.cpu_count() + 2
    sys.path.insert(1, os.path.join(PYCKBASE, 'PyckMaster'))
    sys.path.insert(1, os.path.join(PYCKBASE, 'PyckTool'))
    if args.psswdHash:
        queue = multiprocessing.Queue()
        poison_queue = multiprocessing.Queue()
        suc_queue = multiprocessing.Queue()
        demon = multiprocessing.Process(name='NBDBdaemon', target=notdbd.notdbd, args=(FREAKBASE, queue, poison_queue, POISON_PILL, PILL_COUNT))
        demon.daemon = True
        print '[+] Starting the NotDBD daemon now ...'
        demon.start()
        demon_writer = multiprocessing.Process(name='daemonWriter', target=daemon_writer.writer, args=(CRACKEDLIST, util.getThoseHashes(str(args.psswdHash)), suc_queue, poison_queue, POISON_PILL, PILL_COUNT))
        demon_writer.daemon = True
        print '[+] Starting the writer daemon now ...'
        demon_writer.start()
        print '[+] Starting up super_pyck ...'
        super_pyck.drive(str(args.psswdHash), CRACKEDLIST, FREAKBASE, queue, suc_queue, poison_queue, POISON_PILL, PILL_COUNT, args.verbose)
    elif args.learn:
        if futil.corrupt(args.learn, LEARNED):
            print '[!] The provided password list has been analyzed before.'
            print '[!] Running it again can cause skewed data.'
            decision = raw_input('[!] Would you like to run it anyway? (y/n) ')
            if decision.lower() == 'y':
                super_freak.drive(args.learn, LPYCKBASE, args.verbose)
                futil.log(LEARNED, '%s\n' % args.learn)
        else:
            super_freak.drive(args.learn, LPYCKBASE, args.verbose)
            futil.log(LEARNED, '%s\n' % args.learn)
    elif args.display:
        if args.display == 'Seq':
            futil.showTheFreak(os.path.join(FREAKBASE, '%s.freak' % args.display))
        elif args.display == 'NDBD':
            futil.showTheSpecialFreak(os.path.join(FREAKBASE, '%s.freak' % args.display))
        elif args.display == 'cracked':
            futil.showTheCrack(os.path.join(LPYCKBASE, '%s.freak' % args.display))
        else:
            termDirect = args.display[0]
            futil.showTheFreak(os.path.join(FREAKBASE, termDirect, '%s.freak' % args.display))
    elif args.remove:
        futil.freakyReset(FREAKBASE, LOGBASE)
    else:
        parser.print_help()
    print '[+] LockPyck terminated.'
    return

if __name__ == '__main__':
    main()
