

def triangle_area(a, h):
    """Given length of a side and high return area for a triangle.
    >>> triangle_area(5, 3)
    7.5
    """
    assert isinstance(a, (int, float)) and isinstance(h, (int, float)), "invalid inputs" # $_CONTRACT_$
    assert a > 0 and h > 0, "invalid inputs" # $_CONTRACT_$

    return a * h / 2



METADATA = {}


def check(candidate):
    assert candidate(5, 3) == 7.5
    assert candidate(2, 2) == 2.0
    assert candidate(10, 8) == 40.0


check(triangle_area)