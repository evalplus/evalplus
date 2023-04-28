import time


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

    if record_time:
        return ret, rtime
    else:
        return ret


def trusted_check_exec(code, inputs, entry_point):
    """Check trusted_exec success."""
    try:
        trusted_exec(code, inputs, entry_point)
    except Exception:
        return False
    return True
