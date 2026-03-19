def solve_task4b(string: str) -> str:
    """Returns the shortest word that starts with W"""
    string.replace(",","") 
    words: list = string.split()
    return min((w for w in words if w.startswith('w')), key=len, default="Нет слов на букву w")

