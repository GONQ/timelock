#!/usr/bin/env python2

import timelock
import time

print "TIMELOCK DEBUG TEST."
print "TIMELOCK WILL RUN FOR SEVERAL SECONDS THEN UNLOCK."

seconds = 1
timefile = "time.lock"
id_file = "id.lock"
unlockfile = "open.lock"
debug_flag = True

lockit = timelock.timelock()
unique_id = lockit.dbug(seconds, timefile, id_file, unlockfile, debug_flag)

time.sleep(5)

lockit.unlock(timefile, id_file, unlockfile, unique_id)

print "DEBUG TEST COMPLETE."