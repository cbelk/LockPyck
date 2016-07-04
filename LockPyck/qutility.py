#! /usr/bin/env python

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

# This file contains the functions for interacting with the queues.
#
# Author: Christian Belk

# dumpQueue empties the contents of the queue into a list which is then returned.
def dumpQueue(queue):
    preterms = []
    while not queue.empty():
        preterms.append(queue.get())
    return preterms

# poison is used to put the poison pills in the posion queue.
def poison(poison_queue, pill, pill_count):
    for i in xrange(pill_count):
        poison_queue.put(pill)
    return

# poisoned is used to test whether the poison pill has been entered into the poison_queue.
def poisoned(poison_queue):
    if not poison_queue.empty():
        poison_queue.get(False)
        return True
    return False
