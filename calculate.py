import numpy as np
import json
import graphingfunctions as gf
#value (both x and y), zero, min, max, intersect


config_path = r"C:\Users\Benjamin Mason\3D Objects\Coding\Python\Graphics Calculator\config.json"
with open(config_path, "r") as read_file:
    config = json.load(read_file)

domain = config["domain"]
resolution = config["resolution"] #how many points per 1 unit
N = int((domain[1] - domain[0] + 1) * resolution)




def zeros(function):
    #returns the x values of all zeros
    #aka x intercept

    x = function[0]
    y = function[1]
    n = len(x)
    #because floating point isnt exact:
    #find each point that has a positive y and a negative y as neighbours
    abs_y = np.abs(y)[1:n-1]

    ind = np.arange(0, n)[1:n-1]
    arr = np.vstack((ind, abs_y))
    sorted_arr = arr[:, arr[1].argsort()] #sorts the array by the y values
    #print(sorted_arr)
    #for the bottom few points, check to see if the y values of the points next to them are positive and negative

    y_sign = np.sign(y)
    zeros_arr = np.zeros((0))
    zeros_ind = np.zeros((0))

    for i in range(n-2):
        if y_sign[int(sorted_arr[0, i]-1)] != y_sign[int(sorted_arr[0, i]+1)]:
            #this is a zero
            if 1 in np.abs(zeros_ind - sorted_arr[0, i]):
                continue
            else:
                zeros_arr = np.append(zeros_arr, x[int(sorted_arr[0, i])])
                zeros_ind = np.append(zeros_ind, sorted_arr[0, i])

    return zeros_arr, np.zeros((len(zeros_arr)))


def turnpoints(function):
    #finds the turning points of the function inputted
    x = zeros(gf.nDeriv(function))[0]
    ind = np.zeros((0))

    for i in range(len(x)):
        ind = np.append(ind, np.where(function[0] == x[i])) #for some reason this returns 0 and the correct index

    y = function[1][ind.astype('int')]


    return x, y


def intersect(function1, function2):
    x1, y1 = function1
    x2, y2 = function2

    y_arr = y2 - y1

    x = zeros((x1, y_arr))[0]
    ind = np.zeros((0))

    for i in range(len(x)):
        ind = np.append(ind, np.where(x1 == x[i])) #for some reason this returns 0 and the correct index


    #ind = np.delete(ind, np.arange(0, ind.size, 2))

    y = y1[ind.astype('int')]


    return x, y


def y_intercept(function):
    y, x = zeros(gf.inverse(function))
    return x, y
