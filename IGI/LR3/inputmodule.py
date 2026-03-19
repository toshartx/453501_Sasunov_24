def correct_input(prompt: str = '', datatype: type = str):
    """Provides correct input function specifying the required datatype.\n
       You can also optionally specify a message to accompany the input."""
    while True:
        inputed = input(prompt)
        try:
            return datatype(inputed)
        except ValueError:
            print("Ошибка ввода! Повторите попытку!")
            continue

def input_nums():
    """Provides list of ints input."""
    nums: list = []
    while True:
        num = correct_input("", int)
        if num == 0:
            return nums
        nums.append(num)

def gen_nums():
    """Provides enumerable ints collection input."""
    num = 1                     # ???
    while num != 0:
        num = correct_input("", int)
        yield num