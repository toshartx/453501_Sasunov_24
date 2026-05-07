## Регулярные выражения (Regex)

**Regex** -- это некоторый строковый шаблон для поиска соответствий в тексте. 

d### Базовые конструкции регулярных выражений

| Символ | Применение | Пример |
|------|---------|----------------|
|Обычные цифро-алфавитные символы <br>(например, `б2фl`)|Вхождение символов в тексте| Regex: `3a`<br> Строка: `3a12 4d53ag`<br> Результат:<br> `Match 0-2: 3a`<br>`Match 8-10: 3a`|
|Точка `.`|Вхождение любого символа|Regex: `А.я`<br> Строка: `Аня`<br> Результат:<br> `Match 0-3: Аня`|
**P.s.** Для нахождения конкретно символа точки и других спецсимволов нужно их экранировать (`\.`)
|Множество символов `[]`|Вхождение любого символа из указанного множества. <br> Для указания диапазона символов в скобках требуется использовать `-` (например, запись `[0-9]` позволит найти вхождения цифровых символов из диапазона от 0 до 9)|Regex: `А[нл]я`<br> Строка: `Аня Аля`<br> Результат:<br> `Match 0-3: Аня` <br> `Match 4-7: Аля`|
|Исключение `^` внутри `[]`|Вхождение всех символов, кроме указанных в `[]`|Regex: `А[^н]я`<br> Строка: `Аня Аля`<br> Результат:<br> `Match 4-7: Аля`|
|Перечисление `\|` |Вхождение одного из вариантов| Regex: `Аня\|Аля`<br> Строка: `Аня Аля`<br> Результат:<br> `Match 0-3: Аня` <br> `Match 4-7: Аля`
|Группа символов `()`|Вхождение группы указанных символов **целиком** <br> От `[]` отличается тем, что представляет конкретную группу символов (в то время как `[]` представляет лишь 1)| Regex: `А(нн\|лл\|нгелин)а`<br> Строка: `Ангелина Анна Аля`<br> Результат:<br> `Match 0-8: Ангелина` <br> `Match 9-13: Анна`

Существуют обозначения для основных типов символов (буквенных, цифровых и т.д.)
|Символ|Эквивалент|
|--|--|
|`\d`|`[0-9]`|
|`\D`|`[^0-9]`|
|`\s`|`[ \f\n\r\t\v]` (пробельный символ)|
|`\S`|`[^ \f\n\r\t\v]`|
|`\w`|`[[:word:]]` (буквенный или цифровой символы или знак подчёркивания) |
|`\W`| `[^[:word:]]`(все кроме `\w`) |

`[[:word:]]` -- это обозначение классов символов, один из способов заменить диапазон символов. Их можно посмотреть [здесь](https://habr.com/ru/articles/545150/).

### Квантификаторы

**Квантификаторы** отвечают за количество повторений того или иного символа (группы символов). Квантификаторы ставятся *после* символа. Основные:
|Квантификатор|Значение|
|--|--|
|`*`|Ноль или больше|
|`+`|Одно или больше|
|`?`|Ноль или одно|
|`{n}`|Ровно $n$ раз|
|`{m,n}`|От $m$ до $n$ раз|
|`{m,}`|Более $m$|
|`{,n}`|Менее $n$|

### Границы поиска

По умолчанию **Regex** ищут по включению. Однако порой нам нужно найти конкретное слово, например мы ожидаем, что получим лишь слово `арка`:

```
Regex: арка
Строка: чарка марка арка
Результат: 3 мэтча
```

Для получения нужного нам результата существуют символы проверки границ поиска соответствия. Для данной задачи нам понадобиться символ `\b` который выставляет границу слова:

```
Regex: \bарка\b
Строка: чарка марка арка
Результат: мэтч - арка
```
|Символ проверки границ|Значение|
|-|-|
|`\b`|Граница слова|
|`\B`|Не граница слова|
|`^`|Начало текста (строки)|
|`$`|Конец текста (строки)|

### Группировка

С помощью `()` мы не только обозначаем группу символов, но и даём возможность ссылаться на неё. Например:
```
Regex: <(\w+)><\1> 
# В данном случае, \1 -- ссылка на группу (\w+)
```
Это нам может помочь со строками, которые, например, обладают многим количеством повторов.

Группы также можно именовать с помощью `(?<word>часть_выражения)` или вовсе не захватывать их: `(?:часть_выражения)`

## numpy
```python
# ============================================================================
# NUMPY ШПАРГАЛКА - полный блок кода с комментариями
# ============================================================================

import numpy as np

# ============================================================================
# 1. СОЗДАНИЕ МАССИВОВ
# ============================================================================

# 1.1 Из списков и кортежей
arr1 = np.array([1, 2, 3, 4, 5])                    # одномерный массив
arr2 = np.array([[1, 2, 3], [4, 5, 6]])             # двумерный массив
arr3 = np.array([1, 2, 3], dtype=np.float32)        # с указанием типа
arr4 = np.array((10, 20, 30, 40))                   # из кортежа
arr5 = np.array(range(10))                          # из range

# 1.2 Массивы заданного вида
zeros = np.zeros((2, 3))           # [[0., 0., 0.], [0., 0., 0.]]
ones = np.ones((2, 3))             # [[1., 1., 1.], [1., 1., 1.]]
full = np.full((2, 3), 7)          # [[7, 7, 7], [7, 7, 7]]
empty = np.empty((2, 3))           # массив с мусорными значениями
eye = np.eye(3)                    # единичная матрица 2x2
# [[1., 0., 0.],
#  [0., 1., 0.],
#  [0., 0., 1.]]

# 1.3 Диапазоны и последовательности
arange1 = np.arange(10)            # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
arange2 = np.arange(5, 10)         # [5, 6, 7, 8, 9]
arange3 = np.arange(0, 10, 2)      # [0, 2, 4, 6, 8]
linspace1 = np.linspace(0, 1, 5)   # [0., 0.25, 0.5, 0.75, 1.] (5 равномерных точек)
linspace2 = np.linspace(0, 10, 3)  # [0., 5., 10.]

# 1.4 Случайные массивы
random1 = np.random.rand(3)           # [0.1, 0.7, 0.3] - 3 числа от 0 до 1
random2 = np.random.rand(2, 3)        # 2x3 массив от 0 до 1
random3 = np.random.randint(0, 10)    # одно случайное целое от 0 до 9
random4 = np.random.randint(0, 10, 5) # [2, 7, 1, 9, 4] - 5 случайных целых
random5 = np.random.randint(0, 10, (2, 3))  # 2x3 случайных целых
random6 = np.random.randn(3)          # стандартное нормальное распределение
random7 = np.random.uniform(0, 1, 5)  # равномерное распределение

# 1.5 Изменение формы и копирование
arr = np.array([1, 2, 3, 4, 5, 6])
reshaped = arr.reshape(2, 3)          # [[1, 2, 3], [4, 5, 6]]
reshaped2 = arr.reshape(3, -1)        # автоматический расчет (-1)
flattened = reshaped.flatten()        # [1, 2, 3, 4, 5, 6] - одномерная копия
raveled = reshaped.ravel()            # [1, 2, 3, 4, 5, 6] - одномерное представление
transposed = reshaped.T               # транспонирование [[1, 4], [2, 5], [3, 6]]

# 1.6 Свойства массивов
arr = np.array([[1, 2, 3], [4, 5, 6]])
print(arr.shape)      # (2, 3) - размерность
print(arr.ndim)       # 2 - количество измерений
print(arr.size)       # 6 - общее количество элементов
print(arr.dtype)      # int64 - тип данных
print(arr.itemsize)   # 8 - размер одного элемента в байтах
print(arr.nbytes)     # 48 - общий размер в байтах

# ============================================================================
# 2. ИНДЕКСАЦИЯ И СРЕЗЫ
# ============================================================================

# 2.1 Доступ по индексам
arr = np.array([10, 20, 30, 40, 50])
print(arr[0])          # 10 - первый элемент
print(arr[2])          # 30 - третий элемент
print(arr[-1])         # 50 - последний элемент
print(arr[-2])         # 40 - предпоследний элемент

# 2.2 Индексация в многомерных массивах
arr2d = np.array([[1, 2, 3, 4],
                  [5, 6, 7, 8],
                  [9, 10, 11, 12]])
print(arr2d[0, 1])      # 2 - строка 0, столбец 1
print(arr2d[1])         # [5, 6, 7, 8] - целая строка 1
print(arr2d[1][2])      # 7 - строка 1, столбец 2
print(arr2d[-1, -1])    # 12 - последний элемент

# 2.3 Срезы [start:stop:step]
arr = np.array([0, 10, 20, 30, 40, 50, 60, 70, 80, 90])
print(arr[2:7])         # [20, 30, 40, 50, 60] - с 2 по 6
print(arr[:5])          # [0, 10, 20, 30, 40] - первые 5
print(arr[5:])          # [50, 60, 70, 80, 90] - с 5 до конца
print(arr[::2])         # [0, 20, 40, 60, 80] - каждый второй
print(arr[1::2])        # [10, 30, 50, 70, 90] - каждый второй с 1
print(arr[::3])         # [0, 30, 60, 90] - каждый третий
print(arr[::-1])        # [90, 80, 70, 60, 50, 40, 30, 20, 10, 0] - обратный порядок
print(arr[::-2])        # [90, 70, 50, 30, 10] - обратный каждый второй

# 2.4 Срезы в 2D
arr2d = np.array([[1, 2, 3, 4],
                  [5, 6, 7, 8],
                  [9, 10, 11, 12]])
print(arr2d[0:2, 1:3])    # строки 0-1, столбцы 1-2
# [[2, 3],
#  [6, 7]]
print(arr2d[:, 1:3])      # все строки, столбцы 1-2
print(arr2d[1:, :])       # строки с 1 до конца, все столбцы
print(arr2d[:, ::2])      # все строки, каждый второй столбец
print(arr2d[0:2, :])      # строки 0-1, все столбцы

# 2.5 Индексация с помощью масок (boolean indexing)
arr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
mask = arr > 5
print(mask)               # [False, False, False, False, False, True, True, True, True, True]
print(arr[mask])          # [6, 7, 8, 9, 10] - элементы >5
print(arr[arr % 2 == 0])  # [2, 4, 6, 8, 10] - четные
print(arr[(arr > 3) & (arr < 8)])  # [4, 5, 6, 7] - от 3 до 8

# 2.6 Индексация с помощью списков (fancy indexing)
arr = np.array([10, 20, 30, 40, 50, 60, 70, 80])
indices = [1, 3, 5]
print(arr[indices])       # [20, 40, 60] - элементы по индексам 1,3,5
indices2 = np.array([0, 2, 4, 6])
print(arr[indices2])      # [10, 30, 50, 70]

# ============================================================================
# 3. ОПЕРАЦИИ С МАССИВАМИ
# ============================================================================

# 3.1 Арифметические операции (поэлементные)
a = np.array([1, 2, 3, 4])
b = np.array([5, 6, 7, 8])

print(a + b)      # [6, 8, 10, 12] - сложение
print(a - b)      # [-4, -4, -4, -4] - вычитание
print(a * b)      # [5, 12, 21, 32] - умножение
print(a / b)      # [0.2, 0.333, 0.428, 0.5] - деление
print(a // b)     # [0, 0, 0, 0] - целочисленное деление
print(a % b)      # [1, 2, 3, 4] - остаток от деления
print(a ** 2)     # [1, 4, 9, 16] - возведение в степень
print(a ** b)     # [1, 64, 2187, 65536] - степень
print(-a)         # [-1, -2, -3, -4] - унарный минус

# 3.2 Операции со скаляром
print(a + 10)     # [11, 12, 13, 14]
print(a - 5)      # [-4, -3, -2, -1]
print(a * 3)      # [3, 6, 9, 12]
print(a / 2)      # [0.5, 1., 1.5, 2.]
print(a + 2.5)    # преобразование типов

# 3.3 Сравнения (поэлементные)
print(a > 2)      # [False, False, True, True]
print(a >= 2)     # [False, True, True, True]
print(a < 3)      # [True, True, False, False]
print(a <= 2)     # [True, True, False, False]
print(a == 3)     # [False, False, True, False]
print(a != 3)     # [True, True, False, True]

# 3.4 Логические операции
cond1 = a > 2
cond2 = a < 4
print(cond1 & cond2)        # [False, False, True, False] - И
print(cond1 | cond2)        # [False, True, True, True] - ИЛИ
print(~cond1)               # [True, True, False, False] - НЕ

# 3.5 Универсальные функции (ufunc)
arr = np.array([0, 30, 60, 90])

# Тригонометрические
print(np.sin(np.radians(arr)))    # [0., 0.5, 0.866, 1.]
print(np.cos(np.radians(arr)))    # [1., 0.866, 0.5, 0.]
print(np.tan(np.radians(arr)))    # [0., 0.577, 1.732, inf]
print(np.arcsin(0.5))              # 0.5236 (30°)
print(np.arccos(0.5))              # 1.0472 (60°)
print(np.arctan(1))                # 0.7854 (45°)

# Экспоненциальные и логарифмические
arr = np.array([1, 2, 3, 4])
print(np.exp(arr))         # [2.718, 7.389, 20.085, 54.598] - e^x
print(np.exp2(arr))        # [2., 4., 8., 16.] - 2^x
print(np.log(arr))         # [0., 0.693, 1.099, 1.386] - натуральный логарифм
print(np.log10(arr))       # [0., 0.301, 0.477, 0.602] - десятичный логарифм
print(np.log2(arr))        # [0., 1., 1.585, 2.] - двоичный логарифм
print(np.log1p(arr))       # [0.693, 1.099, 1.386, 1.609] - log(1+x)

# Степени и корни
print(np.sqrt(arr))        # [1., 1.414, 1.732, 2.] - квадратный корень
print(np.square(arr))      # [1, 4, 9, 16] - квадрат
print(np.cbrt(arr))        # [1., 1.26, 1.442, 1.587] - кубический корень
print(np.power(arr, 3))    # [1, 8, 27, 64] - arr^3

# Округление
arr = np.array([1.2, 2.7, 3.5, 4.1, -1.5, -2.6])
print(np.floor(arr))       # [1., 2., 3., 4., -2., -3.] - пол
print(np.ceil(arr))        # [2., 3., 4., 5., -1., -2.] - потолок
print(np.round(arr))       # [1., 3., 4., 4., -2., -3.] - округление
print(np.trunc(arr))       # [1., 2., 3., 4., -1., -2.] - отбрасывание дробной части
print(np.fix(arr))         # [1., 2., 3., 4., -1., -2.] - к нулю

# Абсолютные значения
arr = np.array([-1, -2, 3, -4, 5])
print(np.abs(arr))         # [1, 2, 3, 4, 5]
print(np.absolute(arr))    # [1, 2, 3, 4, 5]

# Знак числа
print(np.sign(arr))        # [-1, -1, 1, -1, 1]

# 3.6 Функции приведения типов
arr = np.array([1.5, 2.7, 3.9])
print(arr.astype(int))     # [1, 2, 3] - преобразование в int
print(arr.astype(str))     # ['1.5', '2.7', '3.9'] - в строки

# ============================================================================
# 4. СТАТИСТИЧЕСКИЕ ФУНКЦИИ
# ============================================================================

# 4.1 mean() - среднее арифметическое
arr = np.array([10, 20, 30, 40, 50])
print(np.mean(arr))                # 30.0
print(arr.mean())                  # 30.0 - метод массива

arr2d = np.array([[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 9]])
print(np.mean(arr2d))              # 5.0 - среднее по всем
print(np.mean(arr2d, axis=0))      # [4., 5., 6.] - по столбцам
print(np.mean(arr2d, axis=1))      # [2., 5., 8.] - по строкам
print(np.mean(arr2d, axis=0, keepdims=True))  # [[4., 5., 6.]] - сохраняет размерность

# 4.2 median() - медиана
arr = np.array([1, 3, 5, 7, 9, 11])
print(np.median(arr))              # 6.0 - среднее 5 и 7
arr_odd = np.array([1, 3, 5, 7, 9])
print(np.median(arr_odd))          # 5.0 - центральный элемент
print(np.median(arr2d))            # 5.0
print(np.median(arr2d, axis=0))    # [4., 5., 6.] - медианы столбцов
print(np.median(arr2d, axis=1))    # [2., 5., 8.] - медианы строк

# 4.3 corrcoef() - коэффициент корреляции
x = np.array([1, 2, 3, 4, 5])
y = np.array([2, 4, 6, 8, 10])
corr = np.corrcoef(x, y)
print(corr)
# [[1. 1.]
#  [1. 1.]] - идеальная положительная корреляция

x2 = np.array([1, 2, 3, 4, 5])
y2 = np.array([10, 8, 6, 4, 2])
print(np.corrcoef(x2, y2))
# [[1., -1.],
#  [-1., 1.]] - идеальная отрицательная корреляция

x3 = np.random.rand(100)
y3 = np.random.rand(100)
print(np.corrcoef(x3, y3)[0, 1])   # ~0.0 - корреляции нет

# Для нескольких переменных
data = np.array([[1, 2, 3],
                 [2, 4, 6],
                 [3, 6, 9]])
print(np.corrcoef(data))           # матрица корреляций 3x3

# 4.4 var() - дисперсия
arr = np.array([10, 20, 30, 40, 50])
print(np.var(arr))                 # 200.0
print(arr.var())                   # 200.0

arr2d = np.array([[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 9]])
print(np.var(arr2d))               # 6.666...
print(np.var(arr2d, axis=0))       # [6., 6., 6.]
print(np.var(arr2d, axis=1))       # [0.666, 0.666, 0.666]
print(np.var(arr, ddof=1))         # 250.0 - для выборки (n-1)

# 4.5 std() - стандартное отклонение
arr = np.array([10, 20, 30, 40, 50])
print(np.std(arr))                 # 14.142135623730951
print(arr.std())                   # 14.142135623730951
print(np.sqrt(np.var(arr)))        # 14.142135623730951 - то же самое

print(np.std(arr2d, axis=0))       # [2.449, 2.449, 2.449]
print(np.std(arr2d, axis=1))       # [0.816, 0.816, 0.816]
print(np.std(arr, ddof=1))         # 15.811388300841896 - выборочное СКО

# 4.6 Другие статистические функции
arr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

print(np.sum(arr))                 # 55 - сумма
print(np.prod(arr))                # 3628800 - произведение
print(np.min(arr))                 # 1 - минимум
print(np.max(arr))                 # 10 - максимум
print(np.argmin(arr))              # 0 - индекс минимума
print(np.argmax(arr))              # 9 - индекс максимума

# Процентили
print(np.percentile(arr, 25))      # 3.25 - 25-й процентиль
print(np.percentile(arr, 50))      # 5.5 - 50-й процентиль (медиана)
print(np.percentile(arr, 75))      # 7.75 - 75-й процентиль
print(np.percentile(arr, [25, 50, 75]))  # [3.25, 5.5, 7.75]

# Квартили
print(np.quantile(arr, 0.25))      # 3.25
print(np.quantile(arr, 0.50))      # 5.5
print(np.quantile(arr, 0.75))      # 7.75

# Размах (range)
print(np.ptp(arr))                 # 9 - max - min

# Кумулятивные суммы и произведения
print(np.cumsum(arr))              # [1, 3, 6, 10, 15, 21, 28, 36, 45, 55]
print(np.cumprod(arr))             # [1, 2, 6, 24, 120, 720, 5040, 40320, 362880, 3628800]

# ============================================================================
# 5. АГРЕГИРУЮЩИЕ ФУНКЦИИ
# ============================================================================

arr2d = np.array([[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 9]])

# Поэлементные функции (агрегации)
print(np.add.reduce(arr2d))        # [12, 15, 18] - сумма по строкам
print(np.add.accumulate(arr2d))    # кумулятивная сумма
print(np.multiply.reduce(arr2d))   # [28, 80, 162] - произведение по строкам

# Специальные агрегации
print(np.trace(arr2d))             # 15 - след матрицы (сумма диагонали)
print(np.diag(arr2d))              # [1, 5, 9] - главная диагональ
print(np.diag(arr2d, k=1))         # [2, 6] - диагональ выше главной
print(np.diag(arr2d, k=-1))        # [4, 8] - диагональ ниже главной

# ============================================================================
# 6. ОПЕРАЦИИ С МАТРИЦАМИ
# ============================================================================

A = np.array([[1, 2],
              [3, 4]])
B = np.array([[5, 6],
              [7, 8]])

# Матричное умножение
print(A @ B)                       # [[19, 22], [43, 50]]
print(np.dot(A, B))                # [[19, 22], [43, 50]]
print(A.dot(B))                    # [[19, 22], [43, 50]]

# Векторное умножение
v = np.array([1, 2])
w = np.array([3, 4])
print(np.dot(v, w))                # 11 - скалярное произведение
print(v @ w)                       # 11

# Свойства матриц
print(np.linalg.det(A))            # -2.0 - определитель
print(np.linalg.inv(A))            # обратная матрица
print(np.linalg.matrix_rank(A))    # 2 - ранг матрицы
print(np.linalg.eig(A))            # собственные значения и векторы
print(np.linalg.norm(A))           # норма матрицы

# Решение систем уравнений
# 2x + 3y = 8
# 4x + 5y = 14
coeff = np.array([[2, 3], [4, 5]])
const = np.array([8, 14])
solution = np.linalg.solve(coeff, const)
print(solution)                    # [1., 2.]

# ============================================================================
# 7. ИЗМЕНЕНИЕ ФОРМЫ И ПРЕОБРАЗОВАНИЯ
# ============================================================================

arr = np.arange(12)
print(arr)                         # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

# Изменение формы
reshaped = arr.reshape(3, 4)       # 3 строки, 4 столбца
print(reshaped)
# [[0, 1, 2, 3],
#  [4, 5, 6, 7],
#  [8, 9, 10, 11]]

reshaped2 = arr.reshape(2, 2, 3)   # 3D массив
reshaped3 = arr.reshape(4, -1)     # автоматический расчет (4, 3)
reshaped4 = arr.reshape(-1, 4)     # (3, 4)

# Транспонирование
matrix = np.array([[1, 2, 3],
                   [4, 5, 6]])
print(matrix.T)
# [[1, 4],
#  [2, 5],
#  [3, 6]]

# Добавление/удаление размерностей
arr2d = np.array([1, 2, 3, 4, 5, 6])
print(arr2d[np.newaxis, :])        # [[1, 2, 3, 4, 5, 6]] - (1, 6)
print(arr2d[:, np.newaxis])        # [[1], [2], [3], [4], [5], [6]] - (6, 1)
print(np.expand_dims(arr2d, axis=0))  # то же самое

# Удаление одномерных записей
arr3d = np.array([[[1, 2, 3]]])
print(arr3d.shape)                 # (1, 1, 3)
print(np.squeeze(arr3d).shape)     # (3,) - убрал размерности 1

# Объединение массивов
a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6], [7, 8]])

print(np.vstack((a, b)))           # вертикальное объединение
# [[1, 2],
#  [3, 4],
#  [5, 6],
#  [7, 8]]

print(np.hstack((a, b)))           # горизонтальное объединение
# [[1, 2, 5, 6],
#  [3, 4, 7, 8]]

print(np.concatenate((a, b), axis=0))  # то же что vstack
print(np.concatenate((a, b), axis=1))  # то же что hstack

# Разделение массивов
arr = np.arange(12).reshape(3, 4)
print(np.split(arr, 3, axis=0))    # разделить на 3 части по вертикали
print(np.split(arr, 2, axis=1))    # разделить на 2 части по горизонтали
print(np.vsplit(arr, 3))           # разделить по вертикали
print(np.hsplit(arr, 2))           # разделить по горизонтали

# ============================================================================
# 8. БЫСТРЫЕ ПРИМЕРЫ ДЛЯ ПОВСЕДНЕВНЫХ ЗАДАЧ
# ============================================================================

# 8.1 Нормализация данных (z-score)
data = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
normalized = (data - np.mean(data)) / np.std(data)
print(normalized)

# 8.2 Масштабирование в диапазон [0, 1]
scaled = (data - np.min(data)) / (np.max(data) - np.min(data))
print(scaled)

# 8.3 Создание тестовых данных
X = np.linspace(0, 2*np.pi, 100)   # 100 точек на периоде
Y = np.sin(X)                       # синусоида

# 8.4 Фильтрация выбросов
data = np.array([1, 2, 100, 3, 4, 200, 5, 6])
mean = np.mean(data)
std = np.std(data)
filtered = data[np.abs(data - mean) < 2 * std]  # отбросить выбросы >2σ
print(filtered)

# 8.5 Поиск уникальных значений
arr = np.array([1, 2, 2, 3, 3, 3, 4, 4, 4, 4])
print(np.unique(arr))              # [1, 2, 3, 4]
print(np.unique(arr, return_counts=True))  # (array([1,2,3,4]), array([1,2,3,4]))

# 8.6 Сортировка
arr = np.array([3, 1, 4, 1, 5, 9, 2, 6])
print(np.sort(arr))                # [1, 1, 2, 3, 4, 5, 6, 9]
print(arr.argsort())               # [1, 3, 6, 0, 2, 4, 7, 5] - индексы сортировки

# 8.7 Broadcasting примеры
a = np.array([[1, 2, 3], [4, 5, 6]])
b = np.array([10, 20, 30])
print(a + b)                       # b "растягивается" до размера a
# [[11, 22, 33],
#  [14, 25, 36]]

# 8.8 Где условие (как тернарный оператор)
arr = np.array([1, 2, 3, 4, 5])
result = np.where(arr > 3, 1, 0)   # [0, 0, 0, 1, 1]
result2 = np.where(arr % 2 == 0, "четное", "нечетное")
print(result2)                     # ['нечетное', 'четное', 'нечетное', 'четное', 'нечетное']

# 8.9 Клиппирование (ограничение значений)
arr = np.array([1, 2, 10, 20, 30, 40, 100])
print(np.clip(arr, 5, 35))         # [5, 5, 10, 20, 30, 35, 35]

# 8.10 Сравнение массивов с допуском (для float)
a = np.array([0.1 + 0.2, 0.3])
b = np.array([0.3, 0.3])
print(np.isclose(a, b))            # [True, True] - сравнение с допуском
print(a == b)                      # [False, True] - точное сравнение

# ============================================================================
# 9. ПОЛЕЗНЫЕ КОНСТАНТЫ
# ============================================================================

print(np.pi)           # 3.141592653589793
print(np.e)            # 2.718281828459045
print(np.inf)          # inf - бесконечность
print(np.nan)          # nan - Not a Number

# Проверка на nan и inf
arr = np.array([1, np.nan, 2, np.inf, 3])
print(np.isnan(arr))   # [False, True, False, False, False]
print(np.isinf(arr))   # [False, False, False, True, False]
print(np.isfinite(arr))# [True, False, True, False, True]

# ============================================================================
# 10. РАБОТА С ПРОПУЩЕННЫМИ ДАННЫМИ (NaN)
# ============================================================================

arr = np.array([1, 2, np.nan, 4, np.nan, 6])
print(np.nanmean(arr))     # 3.25 - среднее без учета NaN
print(np.nanmedian(arr))   # 3.0 - медиана без учета NaN
print(np.nanvar(arr))      # дисперсия без учета NaN
print(np.nanstd(arr))      # СКО без учета NaN
print(np.nansum(arr))      # 13 - сумма без учета NaN

# Замена NaN на другое значение
arr_clean = np.nan_to_num(arr, nan=0)  # [1., 2., 0., 4., 0., 6.]
print(arr_clean)

# Удаление NaN
arr_no_nan = arr[~np.isnan(arr)]       # [1., 2., 4., 6.]
```

## pandas

```py
# ============================================================================
# PANDAS ШПАРГАЛКА - полный блок кода с комментариями
# ============================================================================

import pandas as pd
import numpy as np

# ============================================================================
# 1. СОЗДАНИЕ SERIES И DATAFRAME
# ============================================================================

# 1.1 Series - одномерный массив с индексами
s1 = pd.Series([1, 2, 3, 4, 5])
s2 = pd.Series([1, 2, 3, 4, 5], index=['a', 'b', 'c', 'd', 'e'])
s3 = pd.Series({'a': 1, 'b': 2, 'c': 3})  # из словаря
s4 = pd.Series([1, 2, 3], dtype=float)     # с типом данных

# 1.2 DataFrame - двумерная таблица
# Из списка списков
df1 = pd.DataFrame([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

# Из словаря (ключи = названия столбцов)
df2 = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'City': ['New York', 'London', 'Paris']
})

# Из списка словарей
df3 = pd.DataFrame([
    {'Name': 'Alice', 'Age': 25, 'City': 'NY'},
    {'Name': 'Bob', 'Age': 30, 'City': 'London'},
    {'Name': 'Charlie', 'Age': 35, 'City': 'Paris'}
])

# С указанием индексов строк
df4 = pd.DataFrame(df2.values, index=['row1', 'row2', 'row3'], columns=df2.columns)

# 1.3 Функции создания DataFrame заданного вида
df_zeros = pd.DataFrame(np.zeros((3, 4)))           # из numpy
df_ones = pd.DataFrame(np.ones((2, 3)))             # из numpy
df_range = pd.DataFrame({'A': range(5), 'B': range(5, 10)})
df_random = pd.DataFrame(np.random.rand(3, 4))      # случайные числа

# 1.4 Просмотр информации
print(df2.head(2))       # первые 2 строки
print(df2.tail(2))       # последние 2 строки
print(df2.info())        # информация о DataFrame
print(df2.describe())    # статистика по числовым столбцам
print(df2.shape)         # (3, 3) - строки, столбцы
print(df2.columns)       # Index(['Name', 'Age', 'City'])
print(df2.index)         # RangeIndex(start=0, stop=3, step=1)
print(df2.dtypes)        # типы данных каждого столбца

# ============================================================================
# 2. ИНДЕКСАЦИЯ И СРЕЗЫ
# ============================================================================

df = pd.DataFrame({
    'A': [1, 2, 3, 4, 5],
    'B': [10, 20, 30, 40, 50],
    'C': [100, 200, 300, 400, 500]
})

# 2.1 Выбор столбцов
print(df['A'])           # один столбец -> Series
print(df[['A', 'C']])    # несколько столбцов -> DataFrame
print(df.A)              # то же что df['A'] (если имя без пробелов)

# 2.2 Выбор строк по индексу
print(df.loc[2])         # строка с индексом 2
print(df.loc[1:3])       # строки с 1 по 3 (включительно)
print(df.iloc[0])        # первая строка (по позиции)
print(df.iloc[1:3])      # строки 1 и 2 (по позиции)

# 2.3 Условная выборка
print(df[df['A'] > 3])           # строки где A > 3
print(df[(df['A'] > 2) & (df['B'] < 40)])  # комбинированное условие
print(df[df['C'].isin([200, 400])])        # in условие

# 2.4 loc и iloc (основные методы индексации)
print(df.loc[0:2, 'A':'B'])      # строки 0-2, столбцы A-B
print(df.iloc[0:2, 0:2])         # строки 0-1, столбцы 0-1
print(df.loc[df['A'] > 2, ['A', 'C']])  # условие + нужные столбцы

# 2.5 Атрибуты Series и DataFrame
print(s1.values)         # массив значений [1 2 3 4 5]
print(s1.index)          # индексы
print(s1.name = 'my_series')  # задать имя
print(df.values)         # numpy массив из DataFrame

# ============================================================================
# 3. ОПЕРАЦИИ С ДАННЫМИ
# ============================================================================

# 3.1 Арифметические операции (поэлементно)
df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
print(df + 10)           # прибавить ко всем элементам
print(df * 2)            # умножить все элементы на 2
print(df ** 2)           # возвести в квадрат

# Между DataFrame
df2 = pd.DataFrame({'A': [10, 20, 30], 'B': [40, 50, 60]})
print(df + df2)          # сложение поэлементно

# С Series (broadcast)
s = pd.Series([1, 2], index=['A', 'B'])
print(df + s)            # Series выравнивается по индексам

# 3.2 Работа с пропущенными данными (NaN)
df_nan = pd.DataFrame({
    'A': [1, 2, np.nan, 4],
    'B': [5, np.nan, np.nan, 8],
    'C': [9, 10, 11, 12]
})

print(df_nan.isna())             # проверка на NaN
print(df_nan.isnull())           # то же самое
print(df_nan.dropna())           # удалить строки с NaN
print(df_nan.dropna(axis=1))     # удалить столбцы с NaN
print(df_nan.fillna(0))          # заполнить NaN нулями
print(df_nan.fillna(df_nan.mean()))  # заполнить средним
print(df_nan.interpolate())      # интерполяция

# 3.3 Универсальные функции (можно применять к столбцам)
print(df.apply(np.sum))                     # сумма по столбцам
print(df.apply(lambda x: x.max() - x.min())) # размах по столбцам
print(df['A'].apply(lambda x: x * 2))        # применить к столбцу

# 3.4 map и applymap
print(df['A'].map({1: 'one', 2: 'two', 3: 'three'}))  # замена по словарю
print(df.applymap(lambda x: x * 10))                   # применить ко всем элементам

# 3.5 Добавление и удаление столбцов
df['D'] = [7, 8, 9]                    # добавить столбец
df['E'] = df['A'] + df['B']            # новый столбец из вычислений
df.insert(1, 'New', [100, 200, 300])   # вставить на позицию 1
df.drop('D', axis=1, inplace=True)     # удалить столбец
df.drop(0, axis=0, inplace=True)       # удалить строку

# 3.6 Фильтрация и сортировка
df_sorted = df.sort_values(by='A')              # сортировка по столбцу A
df_sorted = df.sort_values(by=['A', 'B'])       # по нескольким столбцам
df_sorted = df.sort_index(ascending=False)      # сортировка по индексу

# 3.7 Группировка
df_group = pd.DataFrame({
    'Category': ['A', 'A', 'B', 'B', 'C'],
    'Value': [10, 20, 30, 40, 50],
    'Score': [1, 2, 3, 4, 5]
})

grouped = df_group.groupby('Category')
print(grouped.sum())           # сумма по группам
print(grouped.mean())          # среднее по группам
print(grouped.agg(['sum', 'mean', 'count']))  # несколько агрегаций

# ============================================================================
# 4. СТАТИСТИЧЕСКИЕ ФУНКЦИИ
# ============================================================================

df_stats = pd.DataFrame({
    'A': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'B': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
    'C': [5, 3, 8, 2, 9, 1, 7, 4, 6, 10]
})

# 4.1 mean() - среднее арифметическое
print(df_stats.mean())           # среднее по каждому столбцу
print(df_stats.mean(axis=1))     # среднее по строкам
print(df_stats['A'].mean())      # среднее одного столбца

# 4.2 median() - медиана
print(df_stats.median())
print(df_stats['B'].median())

# 4.3 corr() - коэффициент корреляции
print(df_stats.corr())           # матрица корреляций
print(df_stats['A'].corr(df_stats['B']))  # корреляция между A и B

# 4.4 var() - дисперсия
print(df_stats.var())            # дисперсия по столбцам
print(df_stats['A'].var())       # дисперсия одного столбца

# 4.5 std() - стандартное отклонение
print(df_stats.std())
print(df_stats['C'].std())

# 4.6 Другие статистические функции
print(df_stats.sum())            # сумма
print(df_stats.min())            # минимум
print(df_stats.max())            # максимум
print(df_stats.count())          # количество ненулевых значений
print(df_stats.describe())       # все основные статистики сразу

# Квартили и процентили
print(df_stats.quantile(0.25))   # 1-й квартиль
print(df_stats.quantile([0.25, 0.5, 0.75]))  # все квартили

# Кумулятивные функции
print(df_stats.cumsum())         # кумулятивная сумма
print(df_stats.cumprod())        # кумулятивное произведение
print(df_stats.cummax())         # кумулятивный максимум
print(df_stats.cummin())         # кумулятивный минимум

# ============================================================================
# 5. ОБЪЕДИНЕНИЕ И СОЕДИНЕНИЕ ДАННЫХ
# ============================================================================

# 5.1 concat - объединение
df_a = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
df_b = pd.DataFrame({'A': [7, 8, 9], 'B': [10, 11, 12]})

print(pd.concat([df_a, df_b]))               # по вертикали (строки)
print(pd.concat([df_a, df_b], axis=1))       # по горизонтали (столбцы)
print(pd.concat([df_a, df_b], ignore_index=True))  # сбросить индексы

# 5.2 merge - соединение по ключу
left = pd.DataFrame({
    'key': ['A', 'B', 'C'],
    'value_left': [1, 2, 3]
})
right = pd.DataFrame({
    'key': ['A', 'B', 'D'],
    'value_right': [4, 5, 6]
})

print(pd.merge(left, right, on='key'))                # inner join
print(pd.merge(left, right, on='key', how='left'))    # left join
print(pd.merge(left, right, on='key', how='right'))   # right join
print(pd.merge(left, right, on='key', how='outer'))   # outer join

# 5.3 join - соединение по индексу
df1 = pd.DataFrame({'A': [1, 2, 3]}, index=['X', 'Y', 'Z'])
df2 = pd.DataFrame({'B': [4, 5, 6]}, index=['X', 'Y', 'W'])
print(df1.join(df2, how='inner'))

# ============================================================================
# 6. РАБОТА С CSV ФАЙЛАМИ
# ============================================================================

# 6.1 Чтение CSV
# df_csv = pd.read_csv('file.csv')
# df_csv = pd.read_csv('file.csv', sep=';')                    # другой разделитель
# df_csv = pd.read_csv('file.csv', encoding='utf-8')           # кодировка
# df_csv = pd.read_csv('file.csv', index_col=0)                # первый столбец как индекс
# df_csv = pd.read_csv('file.csv', header=None)                # без заголовка
# df_csv = pd.read_csv('file.csv', nrows=100)                  # только 100 строк

# 6.2 Запись в CSV
# df.to_csv('output.csv', index=False)          # без индексов
# df.to_csv('output.csv', encoding='utf-8')     # с кодировкой
# df.to_csv('output.csv', sep=';')              # другой разделитель

# ============================================================================
# 7. БЫСТРЫЕ ПРИМЕРЫ ДЛЯ ПОВСЕДНЕВНЫХ ЗАДАЧ
# ============================================================================

# 7.1 Создание тестовых данных
df_test = pd.DataFrame({
    'date': pd.date_range('2024-01-01', periods=10),
    'value': np.random.randn(10),
    'category': ['A', 'B', 'A', 'B', 'C', 'C', 'A', 'B', 'C', 'A']
})

# 7.2 Установка и сброс индекса
df_test.set_index('date', inplace=True)      # установить дату как индекс
df_test.reset_index(inplace=True)            # сбросить индекс

# 7.3 Переименование столбцов
df_renamed = df_test.rename(columns={'value': 'score', 'category': 'group'})

# 7.4 Обработка дубликатов
df_dup = pd.DataFrame({'A': [1, 1, 2, 2, 3], 'B': [1, 2, 3, 4, 5]})
print(df_dup.duplicated())          # проверка на дубликаты
print(df_dup.drop_duplicates())     # удалить дубликаты
print(df_dup.drop_duplicates(subset=['A']))  # по столбцу A

# 7.5 Pivot tables (сводные таблицы)
df_pivot = pd.DataFrame({
    'Date': ['2024-01-01', '2024-01-01', '2024-01-02', '2024-01-02'],
    'Product': ['A', 'B', 'A', 'B'],
    'Sales': [100, 200, 150, 250]
})
pivot = df_pivot.pivot(index='Date', columns='Product', values='Sales')
print(pivot)

# 7.6 Работа с временными рядами
df_time = pd.DataFrame({
    'date': pd.date_range('2024-01-01', periods=100),
    'value': np.random.randn(100)
})
df_time.set_index('date', inplace=True)
print(df_time.resample('ME').mean())        # помесячная агрегация
print(df_time.rolling(window=7).mean())     # скользящее среднее за 7 дней

# 7.7 Замена значений
df_replace = pd.DataFrame({'A': [1, 2, 3, 4, 5], 'B': ['x', 'y', 'z', 'x', 'y']})
df_replace['A'] = df_replace['A'].replace({1: 10, 2: 20, 3: 30})
df_replace['B'] = df_replace['B'].replace({'x': 'X', 'y': 'Y', 'z': 'Z'})

# 7.8 Работа с категориями
df_cat = pd.DataFrame({'grade': ['A', 'B', 'C', 'A', 'B']})
df_cat['grade'] = pd.Categorical(df_cat['grade'], categories=['A', 'B', 'C'], ordered=True)

# 7.9 Query метод
df_query = pd.DataFrame({'A': [1, 2, 3, 4], 'B': [5, 6, 7, 8], 'C': [9, 10, 11, 12]})
print(df_query.query('A > 2 and B < 8'))
print(df_query.query('C in [9, 11]'))

# 7.10 Memory optimization
print(df_query.memory_usage(deep=True))    # использование памяти
df_optimized = df_query.astype({'A': 'int8', 'B': 'int8', 'C': 'int8'})

# ============================================================================
# 8. РАБОТА С ТЕКСТОВЫМИ ДАННЫМИ
# ============================================================================

df_text = pd.DataFrame({
    'text': ['Hello World', 'Python Pandas', 'Data Analysis', 'Machine Learning'],
    'number': [1, 2, 3, 4]
})

print(df_text['text'].str.lower())           # в нижний регистр
print(df_text['text'].str.upper())           # в верхний регистр
print(df_text['text'].str.contains('Python'))  # содержит подстроку
print(df_text['text'].str.replace(' ', '_'))   # замена
print(df_text['text'].str.split(' '))        # разделение
print(df_text['text'].str.len())             # длина строк

# ============================================================================
# 9. ПОЛЕЗНЫЕ ФУНКЦИИ
# ============================================================================

# 9.1 sample - случайная выборка
print(df_test.sample(n=3))              # 3 случайные строки
print(df_test.sample(frac=0.5))         # 50% строк

# 9.2 nlargest и nsmallest
print(df_stats.nlargest(3, 'A'))        # 3 наибольших по столбцу A
print(df_stats.nsmallest(3, 'B'))       # 3 наименьших по столбцу B

# 9.3 value_counts - подсчет уникальных значений
print(df_test['category'].value_counts())        # частоты
print(df_test['category'].value_counts(normalize=True))  # в долях

# 9.4 unique и nunique
print(df_test['category'].unique())      # уникальные значения
print(df_test['category'].nunique())     # количество уникальных

# 9.5 rank - ранжирование
print(df_stats['A'].rank())              # ранги
print(df_stats['A'].rank(ascending=False))  # обратный порядок

# 9.6 diff и pct_change
print(df_stats['A'].diff())              # разница с предыдущим
print(df_stats['A'].pct_change())        # процентное изменение

# 9.7 where - условная замена
print(df_stats['A'].where(df_stats['A'] > 5, 0))  # >5 оставить, иначе 0

# 9.8 clip - ограничение значений
print(df_stats['A'].clip(3, 8))          # значения от 3 до 8

# ============================================================================
# 10. ПРИМЕРЫ РАБОТЫ С РЕАЛЬНЫМИ ДАННЫМИ
# ============================================================================

# 10.1 Загрузка и быстрый анализ
def quick_analysis(df):
    """Быстрый анализ DataFrame"""
    print(f"Shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print(f"Missing values:\n{df.isna().sum()}")
    print(f"Data types:\n{df.dtypes}")
    print(f"Statistics:\n{df.describe()}")
    return df.info()

# 10.2 Очистка данных
def clean_dataframe(df):
    """Очистка DataFrame"""
    # Удаление дубликатов
    df = df.drop_duplicates()
    
    # Удаление столбцов со всеми NaN
    df = df.dropna(axis=1, how='all')
    
    # Заполнение NaN
    for col in df.select_dtypes(include=[np.number]).columns:
        df[col] = df[col].fillna(df[col].median())
    
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].fillna('Unknown')
    
    return df

# 10.3 Агрегация по группам
def aggregate_by_group(df, group_col, agg_cols):
    """Агрегация по группе"""
    return df.groupby(group_col)[agg_cols].agg(['mean', 'median', 'std', 'count'])

# 10.4 Фильтрация выбросов
def remove_outliers(df, column, n_std=3):
    """Удаление выбросов по n стандартных отклонений"""
    mean = df[column].mean()
    std = df[column].std()
    return df[(df[column] >= mean - n_std * std) & (df[column] <= mean + n_std * std)]

# ============================================================================
# 11. ПРОИЗВОДИТЕЛЬНОСТЬ
# ============================================================================

# 11.1 Использование eval (быстрее чем query)
df_eval = pd.DataFrame({'A': np.random.rand(1000), 'B': np.random.rand(1000)})
result = df_eval.eval('A > 0.5 and B < 0.5')

# 11.2 Использование векторизации вместо циклов
# Медленно:
# for i in range(len(df)):
#     df.loc[i, 'new'] = df.loc[i, 'A'] + df.loc[i, 'B']

# Быстро (векторизовано):
df_eval['new'] = df_eval['A'] + df_eval['B']

# 11.3 Выбор типа данных для экономии памяти
df_mem = pd.DataFrame({
    'int64_default': np.random.randint(0, 100, 1000),
    'int8_optimized': np.random.randint(0, 100, 1000, dtype=np.int8)
})
print(df_mem.memory_usage(deep=True))

# ============================================================================
# 12. КРАТКАЯ ШПАРГАЛКА (САМОЕ ВАЖНОЕ)
# ============================================================================

# Создание
df = pd.DataFrame({'col1': [1, 2, 3], 'col2': [4, 5, 6]})

# Просмотр
df.head()       # первые 5 строк
df.info()       # информация
df.describe()   # статистика

# Выборка
df['col1']                 # один столбец
df[['col1', 'col2']]       # несколько столбцов
df.loc[0]                  # строка по индексу
df.iloc[0]                 # первая строка
df[df['col1'] > 2]         # фильтрация

# Изменение
df['new'] = df['col1'] * 2   # новый столбец
df.drop('new', axis=1)       # удалить столбец
df.rename(columns={'col1': 'new_name'})  # переименовать

# Объединение
pd.concat([df1, df2])        # объединить строки
pd.merge(df1, df2, on='key')  # соединить по ключу

# Статистика
df.mean()        # среднее
df.median()      # медиана
df.std()         # стандартное отклонение
df.var()         # дисперсия
df.corr()        # корреляции

# Группировка
df.groupby('col').mean()

# Пропуски
df.isna().sum()      # количество NaN
df.fillna(0)         # заполнить NaN
df.dropna()          # удалить NaN

# Сохранение
df.to_csv('file.csv', index=False)
```