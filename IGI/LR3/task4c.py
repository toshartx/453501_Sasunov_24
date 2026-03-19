def solve_task4c(string: str):
    """Prints words in descending order of their lengths."""
    string.replace(",","") 
    words: list = string.split()
    words.sort(key=len,reverse=False)
    print(words)