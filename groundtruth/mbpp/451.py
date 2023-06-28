"""
Write a function to remove all whitespaces from the given string.
"""

import re
def remove_whitespaces(text1):
  return (re.sub(r'\s+', '',text1))



assert remove_whitespaces(' Google    Flutter ') == 'GoogleFlutter'
assert remove_whitespaces(' Google    Dart ') == 'GoogleDart'
assert remove_whitespaces(' iOS    Swift ') == 'iOSSwift'
