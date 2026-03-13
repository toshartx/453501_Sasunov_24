from task1 import solve_task1
from task1 import print_in_table
from task2 import solve_task2
from task3 import solve_task3
from task4a import solve_task4a
from task4b import solve_task4b
from task4c import solve_task4c
from inputmodule import correct_input
from inputmodule import gen_nums
from inputmodule import input_nums

def lab_info():
    print("- " * 20, "Лабораторная работа №3", " -" * 20)
    print(f"{'Стандартные типы данных, коллекции, функции, модули':^50}")
    print("Выберите задание для выполнения:")
    print("*","-" * 80,"*")
    print("1. Подсчёт функции f(x) = ln(1-x) с помощью ряда Тейлора;")
    print("2. Подсчёт количества элементов из коллекции, находящиеся в пределе от 5 до 25;")
    print("3. Подсчёт количества пробелов и апострофов в тексте;")
    print("4. Дан текст с запятыми и пробелами в нём. Требуется:")
    print("a. Подсчитать количество слов длиной меньше 6;")
    print("b. Найти наименьшее слово, начинающееся с буквы w;")
    print("c. Вывести список слов в тексте по возрастанию их длины.")
    print("*","-" * 80,"*")
    print()

while True:
    lab_info()
    task = correct_input("Введите номер задания (или введите 0, чтобы завершить программу): ", int)
    if task < 0 and task > 4:
        continue
    elif task == 0:
        print("Программа завершается")
        break
    elif task == 1:
        x = correct_input("Введите x для подсчёта ln(1-x): ", float)
        eps = correct_input("Введите точность подсчёта: ", float)
        result, n = solve_task1(x, eps)
        print_in_table(x, eps, result, n)
        
    elif task == 2:
        while True:
            select_way = correct_input("Введите способ ввода коллекции (1 - обычный пользовательский ввод, 2 - с помощью функции-генератора): ", int)
            if select_way < 1 and select_way > 2:
                continue
            elif select_way == 1:
                nums = input_nums()
                counter = solve_task2(nums)
                print("Количество чисел в диапазоне [5,25]: ", counter)
                break
            elif select_way == 2:
                nums = gen_nums()
                counter = solve_task2(nums)
                print("Количество чисел в диапазоне [5,25]: ", counter)
                break
        
    elif task == 3:
        string = correct_input("Введите строку с пробелами и апострофами: ")
        solve_task3(string)

    elif task == 4:
        string = " Wqwew, FSDfaf rwei hjq. qrq rqras qww wwgkhq rw. 13w"
        print("Количество слов, длиной меньше 6: ", solve_task4a(string))
        print("Наименьшее слово, начинающееся с w: ",solve_task4b(string))
        solve_task4c(string)


