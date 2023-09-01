"""
Write a function to remove uppercase substrings from a given string.
"""

def remove_uppercase(str1):
  assert isinstance(str1, str), "invalid inputs" # $_CONTRACT_$
  return ''.join(c for c in str1 if c.islower())



assert remove_uppercase('cAstyoUrFavoRitETVshoWs') == 'cstyoravoitshos'
assert remove_uppercase('wAtchTheinTernEtrAdIo') == 'wtchheinerntrdo'
assert remove_uppercase('VoicESeaRchAndreComMendaTionS') == 'oiceachndreomendaion'
