# timelock lockfile emulator

- time shifts to stop multiple instances of a script


# ------------------------------------------------------------------------------
+ Timelock is a class for preventing multiple instances of a python script.
+ Timelock mimics file locking without actually having a OS or PID lock.
+ Timelock avoids os-level locking and cross-platform boilerplate.
+ If a script has changed timelock file value in last N seconds timelock aborts.
+ Once invoked timelock will run in a separate thread until application exit(0).
+ The thread checks the lockfiles every N seconds for changes and updates them.
+ When a second instance is spawned it aborts if it finds a fresh timelock file.
# ------------------------------------------------------------------------------

#   USAGE:
    
    To invoke timelock:

    ```
    import timelock
    lockit = timelock()
    unique_id = lockit.startlock(seconds, timefile, id_file, unlockfile)
    ```

    The timelock will run indefinitely and restart itself every N seconds,
    being the seconds value passed to it upon start.
    
    to make your application release the lock and delete the lock files
    immediately upon termination, make this the last command before exit:
    
    ```
    lockit.unlock(timefile, id_file, unlockfile, unique_id)
    ```
    
    Unlock can be fired from anywhere in your code for event handling. It ends
    the timelock thread that was invoked from __FILE__.
    
    Timelock attempts to create the files you pass to it.
    If you pass a filename without path data timelock uses the local directory.
    If you pass a unreachable filepath timelock will raise file exception.
    Debug mode allows to troubleshoot file access issues.

    The 'seconds' variable is integer > 0, eg. 1, 2, 3.
    In most uses the examples shown above are exactly how to implement.
    
    For debug messages output run:
    
    ```
    > $ python timelock.py "debug" seconds, timefile, id_file, unlockfile
    ```
    
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
