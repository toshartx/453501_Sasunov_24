from inputmodule import correct_input

def solve_task5() -> tuple[float, float]:
    """Counts mult of negative elements of list 
    and sum of positive elements that staying before max element by absolute value."""
    nums: list = input_float_nums()

    mul: float = 1.0
    s: float = 0.0
    
    pos_of_max: int = max([(value, i) for i, value in enumerate(nums)], key=lambda x: x[0])[1]

    for i, num in enumerate(nums):
        if num < 0:
            mul *= num
        elif num > 0:
            if i < pos_of_max:
                s += num
    
    return mul, s        

    
    
def input_float_nums() -> list:
    """Provides list of float numbers input."""
    nums_of_elements: int = correct_input("Введите количество элементов списка: ", int)
    nums: list = []
    while nums_of_elements != 0:
        num: float = correct_input('', float)
        nums.append(num)
        nums_of_elements -= 1
    return nums