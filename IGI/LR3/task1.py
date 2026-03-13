# LR3.Task1
# Counts f(x) = ln(1-x) with Taylor Series help
# and print results in table
from math import log

def solve_task1(x, eps = 1e-5) -> float:
    result: float = 0.0
    n: int = 1       
    ln2: float = log(2)   # iteration counter

    arg: float = 1 - x         # ln argument

    if arg < 0.0: 
        raise ValueError("ln arg less than 0")

    while arg >= 2.0:      
        arg /= 2.0
        result += ln2

    adder: float = 1 - arg           # var that adding to result
    while n < 1000 and abs(adder) >= eps:
        adder = pow(1 - arg, n) / float(n)
        result -= adder
        n += 1

    return result, n

def print_in_table(x, eps, result, n):
    print(f"{'x':^10}", f"{'n':^10}", f"{'f(x)':^10}", f"{'math f(x)':^10}", f"{'eps':^10}", sep=" | ")
    print(f"{x:^10.3f}", f"{n:^10}", f"{result:^10.3f}", f"{log(1-x):^10.3f}", f"{eps:^10}", sep=" | ")
    
# result, n = solve_task1(-7.21, 1e-6)
# print_in_table(-7.21, 1e-6, result, n)