from math import log

def solve_task1(x, eps = 1e-5) -> float:
    result: float = 0.0
    n: int = 1       
    ln2: float = math.log(2)   # iteration counter

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


