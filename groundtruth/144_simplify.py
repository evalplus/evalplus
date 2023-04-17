
def simplify(x, n):
    """Your task is to implement a function that will simplify the expression
    x * n. The function returns True if x * n evaluates to a whole number and False
    otherwise. Both x and n, are string representation of a fraction, and have the following format,
    <numerator>/<denominator> where both numerator and denominator are positive whole numbers.

    You can assume that x, and n are valid fractions, and do not have zero as denominator.

    simplify("1/5", "5/1") = True
    simplify("1/6", "2/1") = False
    simplify("7/10", "10/2") = False
    """
    def parse(x): # $_CONTRACT_$
        x_list = x.split("/") # $_CONTRACT_$
        if len(x_list) != 2: return None, None # $_CONTRACT_$
        try: # $_CONTRACT_$
            a, b = int(x_list[0]), int(x_list[1]) # $_CONTRACT_$
        except: return None, None # $_CONTRACT_$
        if b == 0: return None, None # $_CONTRACT_$
        return a, b # $_CONTRACT_$
    x1, y1 = parse(x) # $_CONTRACT_$
    x2, y2 = parse(n) # $_CONTRACT_$
    assert x1 != None and y1 != None and x2 != None and y2 != None, "invalid inputs" # $_CONTRACT_$

    return (x1 * x2) % (y1 * y2) == 0

def check(candidate):

    # Check some simple cases
    assert candidate("1/5", "5/1") == True, 'test1'
    assert candidate("1/6", "2/1") == False, 'test2'
    assert candidate("5/1", "3/1") == True, 'test3'
    assert candidate("7/10", "10/2") == False, 'test4'
    assert candidate("2/10", "50/10") == True, 'test5'
    assert candidate("7/2", "4/2") == True, 'test6'
    assert candidate("11/6", "6/1") == True, 'test7'
    assert candidate("2/3", "5/2") == False, 'test8'
    assert candidate("5/2", "3/5") == False, 'test9'
    assert candidate("2/4", "8/4") == True, 'test10'


    # Check some edge cases that are easy to work out by hand.
    assert candidate("2/4", "4/2") == True, 'test11'
    assert candidate("1/5", "5/1") == True, 'test12'
    assert candidate("1/5", "1/5") == False, 'test13'


check(simplify)