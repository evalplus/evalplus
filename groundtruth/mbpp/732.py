"""
Write a function to replace all occurrences of spaces, commas, or dots with a colon.
"""

import re
def replace_specialchar(text):
 assert isinstance(text, str), "invalid inputs" # $_CONTRACT_$
 return re.sub("[ ,.]", ":", text)




assert replace_specialchar('Python language, Programming language.')==('Python:language::Programming:language:')
assert replace_specialchar('a b c,d e f')==('a:b:c:d:e:f')
assert replace_specialchar('ram reshma,ram rahim')==('ram:reshma:ram:rahim')
