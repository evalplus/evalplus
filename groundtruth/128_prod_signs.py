
def prod_signs(arr):
    """
    You are given an array arr of integers and you need to return
    sum of magnitudes of integers multiplied by product of all signs
    of each number in the array, represented by 1, -1 or 0.
    Note: return None for empty arr.

    Example:
    >>> prod_signs([1, 2, 2, -4]) == -9
    >>> prod_signs([0, 1]) == 0
    >>> prod_signs([]) == None
    """
    if not arr: return None
    prod = 0 if 0 in arr else (-1) ** len(list(filter(lambda x: x < 0, arr)))
    return prod * sum([abs(i) for i in arr])


def check(candidate):

    # Check some simple cases
    assert True, "This prints if this assert fails 1 (good for debugging!)"
    assert candidate([1, 2, 2, -4]) == -9
    assert candidate([0, 1]) == 0
    assert candidate([1, 1, 1, 2, 3, -1, 1]) == -10
    assert candidate([]) == None
    assert candidate([2, 4,1, 2, -1, -1, 9]) == 20
    assert candidate([-1, 1, -1, 1]) == 4
    assert candidate([-1, 1, 1, 1]) == -4
    assert candidate([-1, 1, 1, 0]) == 0

    # Check some edge cases that are easy to work out by hand.
    assert True, "This prints if this assert fails 2 (also good for debugging!)"


check(prod_signs)