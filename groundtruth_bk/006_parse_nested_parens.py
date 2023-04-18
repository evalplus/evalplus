from typing import List


def parse_nested_parens(paren_string: str) -> List[int]:
    """ Input to this function is a string represented multiple groups for nested parentheses separated by spaces.
    For each of the group, output the deepest level of nesting of parentheses.
    E.g. (()()) has maximum two levels of nesting while ((())) has three.

    >>> parse_nested_parens('(()()) ((())) () ((())()())')
    [2, 3, 1, 3]
    """
    cnt = 0 # $_CONTRACT_$
    for ch in paren_string: # $_CONTRACT_$
        assert ch in ["(", ")", " "], "invalid inputs"  # $_CONTRACT_$
        if ch == "(": cnt += 1 # $_CONTRACT_$
        if ch == ")": cnt -= 1 # $_CONTRACT_$
        assert cnt >= 0, "invalid inputs" # $_CONTRACT_$

    res, cnt, max_depth = [], 0, 0
    for ch in paren_string:
        if ch == "(": cnt += 1
        if ch == ")": cnt -= 1
        max_depth = max(max_depth, cnt)
        if cnt == 0:
            if max_depth != 0:
                res.append(max_depth)
                max_depth = 0
    return res



METADATA = {
    'author': 'jt',
    'dataset': 'test'
}


def check(candidate):
    assert candidate('(()()) ((())) () ((())()())') == [2, 3, 1, 3]
    assert candidate('() (()) ((())) (((())))') == [1, 2, 3, 4]
    assert candidate('(()(())((())))') == [4]

check(parse_nested_parens)