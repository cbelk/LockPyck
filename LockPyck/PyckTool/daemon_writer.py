#! /usr/bin/env python

import datetime
import qutility
import time
from NDBD import utility as nutil

def writer(crackedfile, hashlist, suc_queue, poison_queue, poison_pill, pill_count):
    poisoned = False
    with open(crackedfile, 'a+') as crackedout:
        crackedout.write('LockPyck run on %s\n' % datetime.datetime.now())
        while hashlist:
            success = nutil.dumpQueue(suc_queue)
            for succ in success:
                print '\n[+] Hash: %s  ||  Password: %s\n' % (succ[0], succ[1])
                crackedout.write('[+] Hash: %s  ||  Password: %s\n' % (succ[0], succ[1]))
                c = hashlist.count(succ[0])
                while c > 0:
                    hashlist.remove(succ[0])
                    c -= 1
            if poisoned:
                crackedout.close()
                print '[+] Daemon_Writer: Terminating ...'
                return
            if qutility.poisoned(poison_queue):
                print '[+] Daemon_Writer: Recieved poison pill!'
                print '[+] Daemon_writer: Checking for successes one last time ...'
                poisoned = True
            else:
                time.sleep(10)
    crackedout.close()
    print '[+] Cracked all hashes !!!'
    print '[+] Daemon_Writer: Poisoning other LockPyck processes ...'
    qutility.poison(poison_queue, poison_pill, pill_count)
    print '[+] Daemon_Writer: Terminating ...'
    return
