"""
Write a python function to find element at a given index after number of rotations.
"""

def find_Element(arr,ranges,rotations,index) :  
    assert isinstance(arr, list), "invalid inputs" # $_CONTRACT_$
    assert isinstance(ranges, list), "invalid inputs" # $_CONTRACT_$
    assert all(isinstance(x, list) and len(x) == 2 for x in ranges), "invalid inputs" # $_CONTRACT_$
    assert all(isinstance(x, int) for ra in ranges for x in ra), "invalid inputs" # $_CONTRACT_$
    assert isinstance(rotations, int), "invalid inputs" # $_CONTRACT_$
    assert rotations >= 0, "invalid inputs" # $_CONTRACT_$
    assert isinstance(index, int), "invalid inputs" # $_CONTRACT_$
    assert 0 <= index < len(arr), "invalid inputs" # $_CONTRACT_$
    for i in range(rotations - 1,-1,-1 ) : 
        left = ranges[i][0] 
        right = ranges[i][1] 
        if (left <= index and right >= index) : 
            if (index == left) : 
                index = right 
            else : 
                index = index - 1 
    return arr[index] 



assert find_Element([1,2,3,4,5],[[0,2],[0,3]],2,1) == 3
assert find_Element([1,2,3,4],[[0,1],[0,2]],1,2) == 3
assert find_Element([1,2,3,4,5,6],[[0,1],[0,2]],1,1) == 1
