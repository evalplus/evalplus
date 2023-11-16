import time
from evalplus.eval.utils import (
    time_limit,
)

def trusted_exec(code, inputs, entry_point, record_time=False):
    """Execute trusted code in place."""
    exec_globals = {}
    exec(code, exec_globals)
    fn = exec_globals[entry_point]

    rtime = []
    ret = []
    for inp in inputs:
        if record_time:
            start = time.time()
            ret.append(fn(*inp))
            rtime.append(time.time() - start)
        else:
            ret.append(fn(*inp))

    if "check_str" == entry_point or "text_match_three" == entry_point\
       or "text_starta_endb" == entry_point:
        ret = [False if i is None else True for i in ret]

    if record_time:
        return ret, rtime
    else:
        return ret


def trusted_check_exec(code, inputs, entry_point):
    """Check trusted_exec success."""
    try:
        with time_limit(seconds=1.0):
            trusted_exec(code, inputs, entry_point)
    except Exception:
        return False
    return True
