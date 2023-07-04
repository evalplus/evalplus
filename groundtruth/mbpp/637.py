"""
Write a function to check whether the given amount has no profit and no loss
"""

def noprofit_noloss(actual_cost,sale_amount): 
  assert isinstance(actual_cost, (int, float)), "invalid inputs" # $_CONTRACT_$
  assert isinstance(sale_amount, (int, float)), "invalid inputs" # $_CONTRACT_$
  if(sale_amount == actual_cost):
    return True
  else:
    return False



assert noprofit_noloss(1500,1200)==False
assert noprofit_noloss(100,100)==True
assert noprofit_noloss(2000,5000)==False
