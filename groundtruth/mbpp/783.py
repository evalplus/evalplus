"""
Write a function to convert rgb color to hsv color. https://www.geeksforgeeks.org/program-change-rgb-color-model-hsv-color-model/
"""

def rgb_to_hsv(r, g, b):
    assert isinstance(r, (int, float)), "invalid inputs" # $_CONTRACT_$
    assert isinstance(g, (int, float)), "invalid inputs" # $_CONTRACT_$
    assert isinstance(b, (int, float)), "invalid inputs" # $_CONTRACT_$
    assert 0 <= r <= 255, "invalid inputs" # $_CONTRACT_$
    assert 0 <= g <= 255, "invalid inputs" # $_CONTRACT_$
    assert 0 <= b <= 255, "invalid inputs" # $_CONTRACT_$
    import colorsys
    h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
    return (h * 360, s * 100, v * 100)

assert rgb_to_hsv(255, 255, 255)==(0, 0.0, 100.0)
assert rgb_to_hsv(0, 215, 0)==(120.0, 100.0, 84.31372549019608)
assert rgb_to_hsv(10, 215, 110)==(149.2682926829268, 95.34883720930233, 84.31372549019608)
