"""
Write a python function to check whether any value in a sequence exists in a sequence or not.
"""

def overlapping(list1,list2):  
    assert isinstance(list1, list), "invalid inputs" # $_CONTRACT_$
    assert isinstance(list2, list), "invalid inputs" # $_CONTRACT_$
    assert all(isinstance(i, (int, float)) for i in list1), "invalid inputs" # $_CONTRACT_$
    assert all(isinstance(i, (int, float)) for i in list2), "invalid inputs" # $_CONTRACT_$
    for i in range(len(list1)): 
        for j in range(len(list2)): 
            if(list1[i]==list2[j]): 
                return True
    return False



assert overlapping([1,2,3,4,5],[6,7,8,9]) == False
assert overlapping([1,2,3],[4,5,6]) == False
assert overlapping([1,4,5],[1,4,5]) == True
