#! /usr/bin/env python

def poisoned(poison_queue):
    if not poison_queue.empty():
        poison_queue.get(False)
        return True
    return False

def poison(poison_queue, pill, pill_count):
    for i in xrange(pill_count):
        poison_queue.put(pill)
    return
