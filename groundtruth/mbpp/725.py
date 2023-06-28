"""
Write a function to extract values between quotation marks " " of the given string.
"""

import re
def extract_quotation(text1):
  return (re.findall(r'"(.*?)"', text1))



assert extract_quotation('Cortex "A53" Based "multi" tasking "Processor"') == ['A53', 'multi', 'Processor']
assert extract_quotation('Cast your "favorite" entertainment "apps"') == ['favorite', 'apps']
assert extract_quotation('Watch content "4k Ultra HD" resolution with "HDR 10" Support') == ['4k Ultra HD', 'HDR 10']
assert extract_quotation("Watch content '4k Ultra HD' resolution with 'HDR 10' Support") == []
