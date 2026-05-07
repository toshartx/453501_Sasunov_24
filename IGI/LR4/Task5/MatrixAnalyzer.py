import numpy as np

class MatrixAnalyzer:
    def __init__(self, m: int = 5, n: int = 5):
        self.matrix = np.random.randint(-50,50, (m, n))
        print("Случайная матрица:\n", self.matrix)
        
    def change_maxes_in(self, a: int, b: int):
        """Меняет местами максимальные элементы столбцов"""
        try:
            col_1 = self.matrix[:, a]
            col_2 = self.matrix[:, b]
        except IndexError:
            print("Недопустимые индексы")

        max_1,max_2 = max(col_1), max(col_2)
        i, j = list(col_1).index(max_1), list(col_2).index(max_2)
        print(f"Максимальные элементы в столбцах {a}, {b}:", max_1, max_2, sep=' ')
        self.matrix[i, a] = max_2
        self.matrix[j, b] = max_1
        print("Матрица после обмена максимальных элементов:\n", self.matrix)
        
    def correlation_coef(self, a: int, b: int):
        """Вычисляет коэффицент корреляции между элементами столбцов
        Args:
        a - первый столбец
        b - второй столбец
        """
        try:
            col_1 = self.matrix[:, a]
            col_2 = self.matrix[:, b]
        except IndexError:
            print("Недопустимые индексы")

        coef = np.corrcoef(col_1, col_2)
        print("Матрица коэффицентов корреляции между выбранными столбцами:\n", np.round(coef,2))



