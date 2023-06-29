"""
Write a function to sort a list of tuples using the second value of each tuple.
"""

def subject_marks(subjectmarks):
#subject_marks = [('English', 88), ('Science', 90), ('Maths', 97), ('Social sciences', 82)])
 assert isinstance(subjectmarks, list), "invalid inputs" # $_CONTRACT_$
 assert all(isinstance(item, tuple) for item in subjectmarks), "invalid inputs" # $_CONTRACT_$
 assert all(isinstance(item[1], (int, float)) for item in subjectmarks), "invalid inputs" # $_CONTRACT_$
 subjectmarks.sort(key = lambda x: x[1])
 return subjectmarks



assert subject_marks([('English', 88), ('Science', 90), ('Maths', 97), ('Social sciences', 82)])==[('Social sciences', 82), ('English', 88), ('Science', 90), ('Maths', 97)]
assert subject_marks([('Telugu',49),('Hindhi',54),('Social',33)])==([('Social',33),('Telugu',49),('Hindhi',54)])
assert subject_marks([('Physics',96),('Chemistry',97),('Biology',45)])==([('Biology',45),('Physics',96),('Chemistry',97)])
