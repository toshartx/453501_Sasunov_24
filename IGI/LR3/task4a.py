def solve_task4a(string: str) -> int:
    counter: int = 0

    string.replace(",","")            # delete ,
    for word in string.split():        # splitting string
        if word.__len__() < 6:
            counter += 1
    return counter