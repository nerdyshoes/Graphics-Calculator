import numpy as np
import matplotlib.pyplot as plt
import graphingfunctions as gf
import json
import calculate as cal
import time

config_path = r"C:\Users\Benjamin Mason\3D Objects\Coding\Python\Graphics Calculator\config.json"

with open(config_path, "r") as read_file:
    config = json.load(read_file)

fdomain = config["domain"]
resolution = config["resolution"] #how many points per 1 unit
N = int((fdomain[1] - fdomain[0] + 1) * resolution)


#create two numpy arrays, an x and y table, and apply the function to all x



def plot(i, colour="default", domain=[], range=[]):
    if colour == "default":
        plt.plot(i[0], i[1])
    else:
        plt.plot(i[0], i[1], colour)

    if domain != []:
        plt.xlim(domain)
    if range != []:
        plt.ylim(range)
    #plots some function
    #i[0] = x
    #i[1] = y

def plotpoints(i, colour="r"):
    #plots a series of points
    plt.plot(i[0], i[1], colour+"o")

def polf(i):
    t, r = i[0], i[1]
    #polar function

    y = r * np.sin(t)
    x = r * np.cos(t)
    return x, y


def f(x):
    #define some function
    y = x**2 + 2*x
    return x, y

def g(x):
    y = 0 * x**0
    return x, y





class Function:
    def __init__(self, type="cartesian"):
        self.type = type

        if self.type == "polar":
            self.name = "r"
        else:
            self.name = "y"




    def define(self):
        self.defin = input(f"{self.name} = ")
        self.printed = f"{self.type}: {self.name} = {self.defin}"







x = np.linspace(fdomain[0], fdomain[1], N)
t = np.linspace(0, 4 * np.pi, 75)
current_functions = np.array(([])).reshape((0, 3))
n = 1


while True: #main loop
    text = input(">> ")
    text_split = text.split()
    comm = text_split[0]


    if comm == "help":
        help = """
        help        Returns this table.
        exit        Exits the program.
        catalogue   Returns the catalogue.
        define      Define a function.
        graph       Graph all defined functions.
        show        Show all defined functions.
        clear       Clear all currently defined functions.
        edit        Edit a defined function.
        remove      Remove a defined function.
        view_domain Changes the domain.
        view_range  Changes the range.
        """

        print(help)


    elif comm == "exit":
        break


    elif comm == "catalogue":
        catalogue = """
                **Note: all functions are the tuple (x, y)**

                ~~~~~~~graphing functions(.gf):~~~~~~~
        nDeriv(func)            Finds numerical derivative.
        nInt(func)              Finds numerical integral.
        nNthDeriv(func, n)      Finds numerical nth derivative.
        inverse(func)           Finds inverse function.
        arclength(func)         Arclength of a function from x=0



                ~~~~~~~graphing functions(.cal):~~~~~~~
        zeros(func)             Returns coordinates of the zeros.
        turnpoints(func)        Returns coordinates of all turning points.
        intersect(func1, func2) Returns the coodinates of all intersections
                                    between func 1 and func2.
        y_intercept(function)   Returns coodinates of y intercept.


        """

        print(catalogue)


    elif comm == "define":
        if len(text_split) > 1:
            func = Function(text_split[1])
        else:
            func = Function()

        func.define()
        current_functions = np.vstack((current_functions, ([func.name + str(n), func.defin, func])))
        n += 1



    elif comm == "graph": #iterates through current_functions, then shows

        for i in range(current_functions.shape[0]):

            current_type = current_functions[i, 2].type

            if current_type == "cartesian":
                output = eval(current_functions[i, 1])
            elif current_type == "polar":
                #SOMEONE IS ACTUALLY GRAPHING POLAR WTF
                #WHAT A FUCKING CHUMP
                r = eval(current_functions[i, 1])
                output = polf((t, r))
            else:
                output = eval(current_functions[i, 1]) #should work with points




            if type(output) == tuple:
                if current_type == "points":
                    plotpoints(output)

                else:
                    plot(output)

            else:
                plot((x, output))

        plt.show()


    elif comm == "show": #shows all functions currently stored
        print(current_functions)


    elif comm == "clear":
        current_functions = np.array(([])).reshape((0, 3))
        n = 1

    elif comm == "edit":
        print(current_functions)
        func = input("Which to edit? >> ")
        ind = np.where(current_functions[0, :] == func)
        #print(current_functions[ind, :])
        new_func = Function(func)
        new_func.define()
        current_functions[ind, 1] = new_func.defin

    elif comm == "remove":
        print(current_functions)
        func = input("Which to remove? >> ")
        ind = np.where(current_functions[0, :] == func)
        current_functions = np.delete(current_functions, ind, axis=0)

    elif comm == "view_domain":
        lower = input("lower: ")
        upper = input("upper: ")
        plt.xlim([lower, upper])

    elif comm == "view_range":
        lower = input("lower: ")
        upper = input("upper: ")
        plt.ylim([lower, upper])

#main()
