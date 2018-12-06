'''
timelock python library - time shifts to stop multiple instances of a script
(c) 2018, Ber Saxon (GONQ) <auto@eagle.icu> https://eagle.icu

This copyright notice must be retained intact and included with any fork or
distribution of this software. '''

# This is the first concept prototype; kept for reference.

import time
from random import randrange as rnd

def timelock():
    lockfile = "time.lock"
    lox = open(lockfile, 'r')
    combo1 = lox.read()
    time.sleep(1.5)
    combo2 = lox.read()

    if combo1 != combo2:
        print "ANOTHER INSTANCE OF TIMELOCK IS RUNNING. EXITING."
        exit()

    locknums = str(rnd(99999999999999999999999999999999999999999999))

    lox = open(lockfile, 'w')
    lox.write(locknums)
    print "TIMELOCK OBTAINED FILE LOCK."

def lockthread():
  threading.Timer(1.0, lockthread).start()
  timelock()
