"""
Write a function to extract values between quotation marks from a string.
"""

import re
def extract_values(text):
 assert isinstance(text, str), "invalid inputs" # $_CONTRACT_$
 return (re.findall(r'"(.*?)"', text))



assert extract_values('"Python", "PHP", "Java"')==['Python', 'PHP', 'Java']
assert extract_values('"python","program","language"')==['python','program','language']
assert extract_values('"red","blue","green","yellow"')==['red','blue','green','yellow']
