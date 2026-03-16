def correct_input(prompt: str, datatype: type = str):
    while True:
        inputed = input(prompt)
        try:
            return datatype(inputed)
        except ValueError:
            print("Ошибка ввода! Повторите попытку!")
            continue

def input_nums():
    nums: list = []
    while True:
        num = correct_input("", int)
        if num == 0:
            return nums
        nums.append(num)

def gen_nums():
    num = 1                     # ???
    while num != 0:
        num = correct_input("", int)
        yield num