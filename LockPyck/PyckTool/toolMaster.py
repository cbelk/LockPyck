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

import multiprocessing
import pyck

def start_proc ():
    print 'Starting ', multiprocessing.current_process().name

# Test driver for multiprocessing the cutTheKey method. Creates a list of tuples to be passed to cutTheKey. A pool
# is the multiprocessing approach taken here.
def main ():
    passlist = ['b8d0da5cef46f5d015853ea982c4f43b', 'a06bd933e8294b73a777abb26060fa43', 'd1a00fcb151da4cce916a20d3d8fd4d5']
    pretermlist = [['!!','L13','556'], ['L6', '23', '@@'], ['cat', 'D2', '@@'], ['007', 'hat', 'S2']]
    tupls = []
    for each in pretermlist:
        tupls.append((each, passlist,))
#    print tupls
    pool_size = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=pool_size, initializer=start_proc, maxtasksperchild=2,)
    pool_outputs = pool.map(pyck.cutTheKey, tupls)
    pool.close()
    pool.join()

    print 'Results:\n'
    for item in pool_outputs:
        if item:
            print 'hash: %s    password: %s' % (item[0], item[1])

if __name__ == '__main__':
    main()
