from typing import List


def below_zero(operations: List[int]) -> bool:
    """ You're given a list of deposit and withdrawal operations on a bank account that starts with
    zero balance. Your task is to detect if at any point the balance of account fallls below zero, and
    at that point function should return True. Otherwise it should return False.
    >>> below_zero([1, 2, 3])
    False
    >>> below_zero([1, 2, -4, 5])
    True
    """
    assert all([isinstance(v, int) for v in operations]), "invalid inputs" # $_CONTRACT_$
    account = 0
    for operation in operations:
        account += operation
        if account < 0:
            return True
    return False



METADATA = {
    'author': 'jt',
    'dataset': 'test'
}


def check(candidate):
    assert candidate([]) == False
    assert candidate([1, 2, -3, 1, 2, -3]) == False
    assert candidate([1, 2, -4, 5, 6]) == True
    assert candidate([1, -1, 2, -2, 5, -5, 4, -4]) == False
    assert candidate([1, -1, 2, -2, 5, -5, 4, -5]) == True
    assert candidate([1, -2, 2, -2, 5, -5, 4, -4]) == True

check(below_zero)