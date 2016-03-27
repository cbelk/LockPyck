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

import os
import argparse
from PyckMaster import super_freak
from PyckMaster import disp
from PyckMaster import reset

# This is the main driver for LockPyck. It simply takes the command line arguments and calls
# the appropriate method(s) and/or sub-driver(s).
def main ():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--psswdHash', help='specify the absolute path to the file containing the hash(es) to be cracked (one hash per line)')
    parser.add_argument('-l', '--learn', help='specify the absolute path to a file containing plain text passwords to learn from (one password per line)')
    parser.add_argument('-d', '--display', help='specify the freaksheet to display (eg Seq or L6 if avalaible)')
    parser.add_argument('-r', '--remove', action='store_true', help='remove all freaksheets')
    args = parser.parse_args()
    DRIVER = os.path.abspath(__file__)
    PYCKBASE = os.path.dirname(DRIVER)
    LPYCKBASE = PYCKBASE[:-8]
    FREAKBASE = os.path.join(LPYCKBASE, 'FreakSheets')
#    if args.psswdHash and args.learn:
        
#    elif args.passwdHash:

    if args.learn:
        super_freak.main(args.learn, LPYCKBASE)
    elif args.display:
        if args.display == 'Seq':
            disp.showTheFreak(os.path.join(FREAKBASE, '%s.freak' % args.display))
        else:
            termDirect = args.display[0]
            disp.showTheFreak(os.path.join(FREAKBASE, termDirect, '%s.freak' % args.display))
    elif args.remove:
        reset.freakyReset(FREAKBASE)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()