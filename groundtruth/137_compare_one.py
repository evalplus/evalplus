
def compare_one(a, b):
    """
    Create a function that takes integers, floats, or strings representing
    real numbers, and returns the larger variable in its given variable type.
    Return None if the values are equal.
    Note: If a real number is represented as a string, the floating point might be . or ,

    compare_one(1, 2.5) ➞ 2.5
    compare_one(1, "2,3") ➞ "2,3"
    compare_one("5,1", "6") ➞ "6"
    compare_one("1", 1) ➞ None
    """
    def to_val(x): # $_CONTRACT_$
        if type(x) == int or type(x) == float: # $_CONTRACT_$
            return float(x) # $_CONTRACT_$
        if type(x) == str: # $_CONTRACT_$
            std_x = x.replace(",", ".") # $_CONTRACT_$
            try: 
                _ = float(std_x)
            except: return None
            return float(std_x)
        return None
    num_a, num_b = to_val(a), to_val(b) # $_CONTRACT_$
    assert num_a != None and num_b != None, "invalid inputs" # $_CONTRACT_$

    if num_a > num_b:
        return a
    elif num_a == num_b:
        return None
    else:
        return b

def check(candidate):

    # Check some simple cases
    assert candidate(1, 2) == 2
    assert candidate(1, 2.5) == 2.5
    assert candidate(2, 3) == 3
    assert candidate(5, 6) == 6
    assert candidate(1, "2,3") == "2,3"
    assert candidate("5,1", "6") == "6"
    assert candidate("1", "2") == "2"
    assert candidate("1", 1) == None

    # Check some edge cases that are easy to work out by hand.
    assert True


check(compare_one)