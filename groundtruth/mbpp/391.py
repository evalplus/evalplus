"""
Write a function to convert more than one list to nested dictionary.
"""

def convert_list_dictionary(l1, l2, l3):
     assert isinstance(l1, list), "invalid inputs" # $_CONTRACT_$
     assert isinstance(l2, list), "invalid inputs" # $_CONTRACT_$
     assert isinstance(l3, list), "invalid inputs" # $_CONTRACT_$
     result = [{x: {y: z}} for (x, y, z) in zip(l1, l2, l3)]
     return result



assert convert_list_dictionary(["S001", "S002", "S003", "S004"],["Adina Park", "Leyton Marsh", "Duncan Boyle", "Saim Richards"] ,[85, 98, 89, 92])==[{'S001': {'Adina Park': 85}}, {'S002': {'Leyton Marsh': 98}}, {'S003': {'Duncan Boyle': 89}}, {'S004': {'Saim Richards': 92}}]
assert convert_list_dictionary(["abc","def","ghi","jkl"],["python","program","language","programs"],[100,200,300,400])==[{'abc':{'python':100}},{'def':{'program':200}},{'ghi':{'language':300}},{'jkl':{'programs':400}}]
assert convert_list_dictionary(["A1","A2","A3","A4"],["java","C","C++","DBMS"],[10,20,30,40])==[{'A1':{'java':10}},{'A2':{'C':20}},{'A3':{'C++':30}},{'A4':{'DBMS':40}}]
