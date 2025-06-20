# buggy_counter.py

import threading
import time

_current = 0
# using the thread Lock
_t_lock = threading.Lock()


def next_id():
    """Returns a unique ID, incrementing the global counter."""
    # may be get the same time and duplicate value when run in thread
    global _current
    # using the thread Lock that lock the thread access and then release Lock
    # using with to guarantee release the lock
    with _t_lock:
        value = _current
        time.sleep(0)
        _current += 1
        return value

#Solution : Using the thread Lock the controle the thread lock and release
# Taken time : 20 minutes