"""
Write a function that gives loss amount on a sale if the given amount has loss else return 0.
"""

def loss_amount(actual_cost, sale_amount): 
  assert isinstance(actual_cost, (int, float)), "invalid inputs" # $_CONTRACT_$
  assert isinstance(sale_amount, (int, float)), "invalid inputs" # $_CONTRACT_$
  assert actual_cost > 0, "invalid inputs" # $_CONTRACT_$
  assert sale_amount > 0, "invalid inputs" # $_CONTRACT_$
  return max(0, sale_amount - actual_cost)




assert loss_amount(1500,1200)==0
assert loss_amount(100,200)==100
assert loss_amount(2000,5000)==3000
