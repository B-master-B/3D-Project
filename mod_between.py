import numpy as np

def mod_between(x, per):
    xbar = x/per - 0.5
    frac = xbar - np.floor(xbar)
    return (frac - 0.5)*per

# x = np.array(range(-100, 100, 10))
# print(mod_between(x, 80))
