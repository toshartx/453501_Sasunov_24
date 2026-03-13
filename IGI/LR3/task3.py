def decor(func):
    def inner(*args, **kwargs):
        print("-" * 20, "Результаты анализа", "-" * 20)
        result = func(*args, **kwargs)
        print(result[0], " - пробелы,", result[1], " - апострофы.")
    return inner 

@decor
def solve_task3(string: str):
    spaces = 0
    apostrophes = 0

    for char in string:
        if char == " ":
            spaces += 1
        if char == "'":
            apostrophes += 1

    return spaces, apostrophes

solve_task3("  ssd ' sa wq  ' ''")
