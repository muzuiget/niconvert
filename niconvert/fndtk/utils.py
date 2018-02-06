import sys
import traceback
from time import time as mktime
from datetime import datetime
from contextlib import contextmanager

def toisotime(timestamp=None):
    if timestamp is None:
        timestamp = mktime()
    timezone_hour = 8
    isotime_format = '%Y-%m-%d %H:%M:%S'
    offset = 3600 * timezone_hour
    dt = datetime.utcfromtimestamp(timestamp + offset)
    return datetime.strftime(dt, isotime_format)

@contextmanager
def redirect_stdio(stream):
    orig_stdout = sys.stdout
    orig_stderr = sys.stderr
    sys.stdout = stream
    sys.stderr = stream
    try:
        yield
    except Exception: # pylint: disable=broad-except
        print(traceback.format_exc())
    sys.stdout = orig_stdout
    sys.stderr = orig_stderr
