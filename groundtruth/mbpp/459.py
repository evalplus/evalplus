"""
Write a function to remove uppercase substrings from a given string.
"""

import re
def remove_uppercase(str1):
  return re.sub('[A-Z]', '', str1)



assert remove_uppercase('cAstyoUrFavoRitETVshoWs') == 'cstyoravoitshos'
assert remove_uppercase('wAtchTheinTernEtrAdIo') == 'wtchheinerntrdo'
assert remove_uppercase('VoicESeaRchAndreComMendaTionS') == 'oiceachndreomendaion'
