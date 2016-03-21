#! /usr/bin/env python

import os
import super_freak

crackstation_dir = '' #put in the absolute path to the p1 directory you have
for passlist in os.listdir(crackstation_dir):
    super_freak.main(passlist)
