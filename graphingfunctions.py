import numpy as np
import numpy.ma as ma
import json
import time


config_path = r"C:\Users\Benjamin Mason\3D Objects\Coding\Python\Graphics Calculator\config.json"
with open(config_path, "r") as read_file:
    config = json.load(read_file)

domain = config["domain"]
resolution = config["resolution"] #how many points per 1 unit
N = int((domain[1] - domain[0] + 1) * resolution)



def choose(n, r):
    x = np.math.factorial(n)/(np.math.factorial(r) * np.math.factorial(n - r))
    return x

def nDeriv(function):
    #numerical derivative
    #using the technique symmetric difference quotient
    #essentially finds the derivative by taking the difference on either side of x
    #and dividing by 2h
    #https://en.wikipedia.org/wiki/Numerical_differentiation
    x, y = function
    h = (np.abs(domain[1] - domain[0]) + 1) / N

    dydx = (y[2:] - y[:N-2]) / (2*h)
    new_x = x[1:N-1]

    return new_x, dydx


def nIntOld(function):
    start_time = time.time()
    #numerical integration
    #this is just a Left Riemann sum, not too hard but a bit annoying
    #https://en.wikipedia.org/wiki/Numerical_integration
    #the harder stuff is too hard for this late at night, maybe redo this
    x, y = function
    h = (np.abs(domain[1] - domain[0]) + 1) / N

    areas = h * y
    mask = np.sign(x)
    mask[mask == 0] = 1
    mask[mask == -1] = 0

    neg_areas = ma.masked_array(areas, mask=mask).compressed()
    neg_F = np.cumsum(neg_areas[::-1])[::-1] * -1

    #swapped_mask = -1 * mask + 1
    swapped_mask = np.logical_not(mask)
    pos_areas = ma.masked_array(areas, mask=swapped_mask).compressed()
    pos_F = np.cumsum(pos_areas)

    F = ma.concatenate((neg_F, pos_F))
    print(f"unoptimized: {time.time() - start_time}")
    return x, F


def nInt(function):
    start_time = time.time()


    x, y = function
    h = (np.abs(domain[1] - domain[0]) + 1) / N

    i = np.where(x >= 0)
    j = np.where(x < 0)
    pos_y = y[i]
    neg_y = y[j]

    pos_cumsum = np.cumsum(pos_y)
    neg_cumsum = np.cumsum(neg_y[::-1])[::-1] * -1

    F = np.concatenate([neg_cumsum, pos_cumsum]) * h


    print(f"optimized: {time.time() - start_time}")


    return x, F





def nNthDeriv(function, n):
    #finds the nth derivative of a function
    #not the most accurate, but pretty good for how easy it is
    #https://en.wikipedia.org/wiki/Numerical_differentiation

    #to improve: https://math.stackexchange.com/questions/130192/method-for-estimating-the-nth-derivative

    #something went wrong with f(x)=x, n=10
    x, y = function
    h = (np.abs(domain[1] - domain[0]) + 1) / N
    #print(h)
    y_arr = np.zeros(y[:N-n].shape)

    for k in range(n+1):
        #s is the current y value for the kth thing
        s = (-1)**(k+n) * choose(n, k) * y[k:N-(n-k)]

        y_arr += s

    y_arr = y_arr / (h**n)
    new_x = x[:N-n]


    return new_x, y_arr


def inverse(function):
    #finds inverse function
    x, y = function
    return y, x



def arclength(function):
    #finds arclength "function"
    x, y = nDeriv(function)
    integrand = np.sqrt(1 + y**2)
    arclength_x, arclength_y = nInt((x, integrand))
    return arclength_x, arclength_y
