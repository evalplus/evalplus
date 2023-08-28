"""
Write a function to find the minimum product from the pairs of tuples within a given list.
"""

def min_product_tuple(list1):
    assert isinstance(list1, list), "invalid inputs" # $_CONTRACT_$
    assert len(list1) > 0, "invalid inputs" # $_CONTRACT_$
    assert all(isinstance(ele, tuple) for ele in list1), "invalid inputs" # $_CONTRACT_$
    assert all(isinstance(ele, (int, float)) for sub in list1 for ele in sub), "invalid inputs" # $_CONTRACT_$
    return min(x * y for x, y in list1)



assert min_product_tuple([(2, 7), (2, 6), (1, 8), (4, 9)] )==8
assert min_product_tuple([(10,20), (15,2), (5,10)] )==30
assert min_product_tuple([(11,44), (10,15), (20,5), (12, 9)] )==100
