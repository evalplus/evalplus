"""
Write a function that counts the number of pairs of integers in a list that xor to an even number.
"""

def find_even_pair(A): 
  assert isinstance(A, list), "invalid inputs" # $_CONTRACT_$
  assert all(isinstance(x, int) for x in A), "invalid inputs" # $_CONTRACT_$
  if len(A) < 2: 
    return 0
  return sum((a ^ b) % 2 == 0 for i, a in enumerate(A) for b in A[i + 1:])



assert find_even_pair([5, 4, 7, 2, 1]) == 4
assert find_even_pair([7, 2, 8, 1, 0, 5, 11]) == 9
assert find_even_pair([1, 2, 3]) == 1
