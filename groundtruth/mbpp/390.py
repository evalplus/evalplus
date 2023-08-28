"""
Write a function to apply a given format string to all of the elements in a list.
"""

def add_string(list_, string):
    assert isinstance(list_, list), "invalid inputs" # $_CONTRACT_$
    assert isinstance(string, str), "invalid inputs" # $_CONTRACT_$
    return [string.format(i) for i in  list_]



assert add_string([1,2,3,4],'temp{0}')==['temp1', 'temp2', 'temp3', 'temp4']
assert add_string(['a','b','c','d'], 'python{0}')==[ 'pythona', 'pythonb', 'pythonc', 'pythond']
assert add_string([5,6,7,8],'string{0}')==['string5', 'string6', 'string7', 'string8']
