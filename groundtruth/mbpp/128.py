"""
Write a function to find words that are longer than n characters from a given list of words.
"""

def long_words(n, s):
    assert isinstance(n, int), "invalid inputs" # $_CONTRACT_$
    assert isinstance(s, str), "invalid inputs" # $_CONTRACT_$
    assert n >= 0, "invalid inputs" # $_CONTRACT_$
    word_len = []
    txt = s.split(" ")
    for x in txt:
        if len(x) > n:
            word_len.append(x)
    return word_len	



assert long_words(3,"python is a programming language")==['python','programming','language']
assert long_words(2,"writing a program")==['writing','program']
assert long_words(5,"sorting list")==['sorting']
