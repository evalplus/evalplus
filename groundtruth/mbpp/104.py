"""
Write a function to sort each sublist of strings in a given list of lists.
"""

def sort_sublists(input_list):
    assert isinstance(input_list, (list, tuple)), "invalid inputs" # $_CONTRACT_$
    assert all(isinstance(x, list) for x in input_list), "invalid inputs" # $_CONTRACT_$
    assert all(all(isinstance(y, str) for y in x) for x in input_list), "invalid inputs" # $_CONTRACT_$
    result = [sorted(x, key = lambda x:x[0]) for x in input_list] 
    return result




assert sort_sublists((["green", "orange"], ["black", "white"], ["white", "black", "orange"]))==[['green', 'orange'], ['black', 'white'], ['black', 'orange', 'white']]
assert sort_sublists(([" red ","green" ],["blue "," black"],[" orange","brown"]))==[[' red ', 'green'], [' black', 'blue '], [' orange', 'brown']]
assert sort_sublists((["zilver","gold"], ["magnesium","aluminium"], ["steel", "bronze"]))==[['gold', 'zilver'],['aluminium', 'magnesium'], ['bronze', 'steel']]
