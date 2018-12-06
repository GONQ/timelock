#!/usr/bin/env python3

# timelock python library - time shifts to stop multiple instances of a script
# (c) 2018, Ber Saxon (GONQ) <auto@eagle.icu> https://eagle.icu

# License: use or redistribution subject to license included herewith.
# This copyright notice must be included with any fork or distribution.

# ------------------------------------------------------------------------------

# Timelock is a class for preventing multiple instances of a python script.
# Timelock mimics file locking without actually having a OS or PID lock.
# Timelock avoids os-level locking and cross-platform boilerplate.
# If a script has changed timelock file value in last N seconds timelock aborts.
# Once invoked timelock will run in a separate thread until application exit(0).
# The thread checks the lockfiles every N seconds for changes and updates them.
# When a second instance is spawned it aborts if it finds a fresh timelock file.

# ------------------------------------------------------------------------------

''' usage:
    
    To invoke timelock:

    import timelock
    lockit = timelock()
    unique_id = lockit.startlock(seconds, timefile, id_file, unlockfile)

    The timelock will run indefinitely and restart itself every N seconds,
    being the seconds value passed to it upon start.
    
    to make your application release the lock and delete the lock files
    immediately upon termination, make this the last command before exit:
    
    lockit.unlock(timefile, id_file, unlockfile, unique_id)
    
    Unlock can be fired from anywhere in your code for event handling. It ends
    the timelock thread that was invoked from __FILE__.
    
    Timelock attempts to create the files you pass to it.
    If you pass a filename without path data timelock uses the local directory.
    If you pass a unreachable filepath timelock will raise file exception.
    Debug mode allows to troubleshoot file access issues.

    The 'seconds' variable is integer > 0, eg. 1, 2, 3.
    In most uses the examples shown above are exactly how to implement.
    
    For debug messages output run:
    
    > $ python timelock.py "debug" seconds, timefile, id_file, unlockfile

    Incomplete breakdown of actions and items used to mimic file locking:
    
# ------------------------------------------------------------------------------
    1 Put random ID in id_file.
    2 Put time.time() in timefile.
    3 Create a timer thread to check the files every N seconds.
    4 Write new time to lockfile this every N seconds.
    5 New instances read the values and compare the time span of last write.
    6 If more than N seconds has passed, new instance re-writes the files.

# ------------------------------------------------------------------------------    
    checklock() : check if lock exists, die on True
    writetimelock() : if lock not exist, activate new lock and run
    echo() : call print with CLI debug function
    unlock() : remove timelock files and kill the current thread
    writeid() : write a new id_file and unique_id upon startup
    checkid() : check the id_file for existence or change
    checklock() : check the epoch time in timefile - if gap is 1s or more, run
    lockthread() : python threading to bootstrap the loop every N seconds
    startlock() : the call function that passes parameters to the class    '''

################################################################################

import threading
import random
import time
import sys
import os

# ------------------------------------------------------------------------------ 
class timelock:
        
    def echo(self, message):
        if self.debug == True:
            print(message)
        else:
            message = ''

# ------------------------------------------------------------------------------
    def unlock(self, timefile, id_file, unlockfile, unique_id):
        self.timefile = timefile
        self.id_file = id_file
        self.unlockfile = unlockfile
        self.unique_id = unique_id
        
        lockfile = id_file
        
        unlox = open(self.unlockfile, 'w')
        unlox.write(self.unique_id)
        unlox.close()        
        if os.path.exists(lockfile):
            os.remove(lockfile)
            if self.debug == True:
                self.echo("UNLOCKED ID FILE")
                self.echo(timelock.counter)
        if os.path.exists(timelock.timefile):
            os.remove(timelock.timefile)
            if self.debug == True:
                self.echo("UNLOCKED TIME FILE")
            os._exit(0)

# ------------------------------------------------------------------------------            
    def writeid(self):
        lockfile = timelock.id_file
        idx = open(lockfile, 'w')
        idx.write(timelock.unique_id)
        if self.debug == True:
            self.echo( "WROTE UNIQUE ID " + timelock.unique_id )

# ------------------------------------------------------------------------------
    def checkid(self):
        lockfile = timelock.id_file
        if os.path.isfile(lockfile):
            idx = open(lockfile, 'r')
            ident1 = idx.read()
            if ident1 != timelock.unique_id:
                if self.debug == True:
                    echo( "UNIQUE ID HAS CHANGED. ANOTHER INSTANCE TOOK LOCK. EXITING." )
                os._exit(0)
        elif timelock.counter > 0:
            os._exit(0)
        else:
            self.writeid()

# ------------------------------------------------------------------------------
    def checklock(self):
        if os.path.isfile(timelock.timefile):
            lockfile1 = timelock.timefile

            lockx = open(lockfile1, 'r')
            clock1 = lockx.read()
            
            now = int(str(time.time())[0:10])
            past = int(clock1)

            if now - past < ( timelock.seconds + 1):
                if self.debug == True:
                    self.echo ( "ANOTHER INSTANCE OF TIMELOCK IS RUNNING. EXITING." )
                os._exit(0)
            else:
                if self.debug == True:
                    self.echo ( "NO OTHER INSTANCE DETECTED. RUNNING THE TIMELOCK." )

# ------------------------------------------------------------------------------
    def writetimelock(self):
        clock = str(time.time())[0:10]
        lockfile1 = timelock.timefile
        lox = open(lockfile1, 'w')
        lox.write(clock)
        if self.debug == True:
            self.echo ( "TIMELOCK OBTAINED PRECEDENCE. " + str(time.time())[0:10] )
        self.checkid()

# ------------------------------------------------------------------------------
    def lockthread(self):
        threading.Timer(timelock.seconds, self.lockthread).start()

        if os.path.exists(timelock.unlockfile):
            unlox = open(timelock.unlockfile, 'r')
            id_test = unlox.read()
            unlox.close()
            if id_test == timelock.unique_id:
                os.remove(timelock.unlockfile)
                if os.path.exists(timelock.timefile):
                    os.remove(timelock.timefile)
                    if os.path.exists(timelock.id_file):
                        os.remove(timelock.id_file)
                        os._exit(0)
        self.writetimelock()
        timelock.counter += 1

# ------------------------------------------------------------------------------
    def startlock(self, seconds, timefile, id_file, unlockfile):
    
        # initialize this variable at 0, increment as a counter
        # if greater than zero and unique_id file changes, break the lock
        timelock.counter = 0
 
        mode = sys.argv
        if "debug" in mode:
            timelock.debug = True
        else:
            timelock.debug = False

        timelock.unique_id = str(random.randrange(
        1000000000000000000000000000000000000000000000000000000000000000,
        9999999999999999999999999999999999999999999999999999999999999999 ))
        
        timelock.seconds = seconds
        timelock.timefile = timefile
        timelock.id_file = id_file
        timelock.unlockfile = unlockfile
        self.checklock()
        self.writeid()
        self.lockthread()
        return timelock.unique_id

# ------------------------------------------------------------------------------
    def dbug(self, seconds, timefile, id_file, unlockfile, debug_flag):
    
        # initialize this variable at 0, increment as a counter
        # if greater than zero and unique_id file changes, break the lock
        timelock.counter = 0
        self.debug_flag = debug_flag
 
        if self.debug_flag == True:
            timelock.debug = True
        else:
            timelock.debug = False

        timelock.unique_id = str(random.randrange(
        1000000000000000000000000000000000000000000000000000000000000000,
        9999999999999999999999999999999999999999999999999999999999999999 ))
        
        timelock.seconds = seconds
        timelock.timefile = timefile
        timelock.id_file = id_file
        timelock.unlockfile = unlockfile
        self.checklock()
        self.writeid()
        self.lockthread()
        return timelock.unique_id
# ------------------------------------------------------------------------------
# CLI debug mode - allows test arguments

# ------------------------------------------------------------------------------
if "debug" in sys.argv:
    if len(sys.argv) != 6:
        print("debug mode requires these arguments:")
        print("==> 'debug' seconds timefile id_file unlockfile")
    if len(sys.argv) == 6:
        args = sys.argv
        print("arguments: ", args[2], args[3], args[4], args[5])
        dbug = timelock()
        unique = dbug.startlock(int(args[2]), args[3], args[4], args[5])
        print("UNIQUE ID: ", unique)
