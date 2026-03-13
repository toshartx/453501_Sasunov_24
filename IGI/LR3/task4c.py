def solve_task4c(string: str):
    string.replace(",","") 
    words: list = string.split()
    words.sort(key=len,reverse=False)
    print(words)

solve_task4c("awd tqewt gkk eoq offf wqqqqe3")