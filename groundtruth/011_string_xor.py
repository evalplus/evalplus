from typing import List


def string_xor(a: str, b: str) -> str:
    """ Input are two strings a and b consisting only of 1s and 0s.
    Perform binary XOR on these inputs and return result also as a string.
    >>> string_xor('010', '110')
    '100'
    """
    assert isinstance(a, str) and isinstance(b, str), "invalid inputs" # $_CONTRACT_$
    assert len(a) == len(b), "invalid inputs" # $_CONTRACT_$
    assert set(a).issubset({"0", "1"}) and set(b).issubset({"0", "1"}), "invalid inputs" # $_CONTRACT_$

    return "".join(str(int(a[i]) ^ int(b[i])) for i in range(len(a)))



METADATA = {
    'author': 'jt',
    'dataset': 'test'
}


def check(candidate):
    assert candidate('111000', '101010') == '010010'
    assert candidate('1', '1') == '0'
    assert candidate('0101', '0000') == '0101'

check(string_xor)