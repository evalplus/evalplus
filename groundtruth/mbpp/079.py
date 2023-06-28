"""
Write a python function to check whether the length of the word is odd or not.
"""

def word_len(s): 
    s = s.split(' ')   
    for word in s:    
        if len(word)%2!=0: 
            return True  
        else:
          return False



assert word_len("Hadoop") == False
assert word_len("great") == True
assert word_len("structure") == True
