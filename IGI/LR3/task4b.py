def solve_task4b(string: str) -> str:
    string.replace(",","") 
    words: list = string.split()
    return min((w for w in words if w.startswith('w')), key=len, default="Нет слов на букву w")

