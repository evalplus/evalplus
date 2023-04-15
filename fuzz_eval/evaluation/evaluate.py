from fuzz_eval.evaluation.evaluate_helpers import (
    TimeoutException,
    create_tempdir,
    reliability_guard,
    swallow_io,
    time_limit,
)


def construct_inputs_sig(inputs: list) -> str:
    str_builder = ""
    for x in inputs:
        if type(x) == str:
            str_builder += f"'{x}',"
        else:
            str_builder += f"{x},"
    return str_builder[:-1]


def evaluate(code: str, inputs: list, signature: str) -> str:

    eval_code = code + f"\noutputs = {signature}({construct_inputs_sig(inputs)})"
    exec_globals = {}

    def unsafe_execute():
        with create_tempdir():
            # These system calls are needed when cleaning up tempdir.
            import os
            import shutil

            rmtree = shutil.rmtree
            rmdir = os.rmdir
            chdir = os.chdir
            # Disable functionalities that can make destructive changes to the test.
            reliability_guard()
            # Construct the check program and run it.
            check_program = eval_code
            try:
                with swallow_io():
                    with time_limit(1):
                        exec(check_program, exec_globals)
            except TimeoutException:
                exec_globals["outputs"] = "timed out"
                pass
            except BaseException as e:
                exec_globals["outputs"] = "thrown exception"
                pass
            # Needed for cleaning up.
            shutil.rmtree = rmtree
            os.rmdir = rmdir
            os.chdir = chdir

    # todo apply multi-threads
    unsafe_execute()
    return exec_globals["outputs"]


if __name__ == "__main__":
    # sanity.
    code = '''
def is_palindrome(string: str) -> bool:
    """ Test if given string is a palindrome """
    return string == string[::-1]


def make_palindrome(string: str) -> str:
    """ Find the shortest palindrome that begins with a supplied string.
    Algorithm idea is simple:
    - Find the longest postfix of supplied string that is a palindrome.
    - Append to the end of the string reverse of a string prefix that comes before the palindromic suffix.
    >>> make_palindrome('')
    ''
    >>> make_palindrome('cat')
    'catac'
    >>> make_palindrome('cata')
    'catac'
    """

    if is_palindrome(string):
        return string
    for i in range(len(string)):
        if is_palindrome(string[i:]):
            return string + string[i-1::-1]
    '''
    o = evaluate(code, ["cata"], "make_palindrome")
    assert o == "catac"
