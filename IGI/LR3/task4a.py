def solve_task4a(string: str) -> int:
    counter: int = 0

    string.replace(",","")            # delete ,
    for word in string.split():        # splitting string
        if word.count < 6:
            counter += 1
    return counter