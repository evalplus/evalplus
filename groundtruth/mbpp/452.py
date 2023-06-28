"""
Write a function that gives loss amount on a sale if the given amount has loss else return 0.
"""

def loss_amount(actual_cost,sale_amount): 
  if(sale_amount > actual_cost):
    amount = sale_amount - actual_cost
    return amount
  else:
    return 0



assert loss_amount(1500,1200)==0
assert loss_amount(100,200)==100
assert loss_amount(2000,5000)==3000
