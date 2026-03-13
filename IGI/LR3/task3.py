def solve_task3(string: str):
    spaces = 0
    apostrophes = 0

    for char in string:
        if char == " ":
            spaces += 1
        if char == "'":
            apostrophes += 1

    return spaces, apostrophes


