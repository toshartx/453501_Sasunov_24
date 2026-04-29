import math
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter

class SeriesAnalyzer:
    def __init__(self, x_start: float, x_end: float, x_step: float, n_terms: int):
        """
        Инициализация анализатора
        
        Args:
            x_start: начальное значение x
            x_end: конечное значение x
            x_step: шаг изменения x
            n_terms: количество членов ряда для суммирования
        """ 
        self.x_start = x_start
        self.x_end = x_end
        self.x_step = x_step
        self.n_terms = n_terms
        self.x_values = []
        self.f_series_values = []  
        self.f_math_values = []   
        self.results = {}

    def generate_data(self) -> None:
        """Генерация данных для анализа"""
        x = self.x_start
        
        while x <= self.x_end + self.x_step / 2: 
            self.x_values.append(x)
            self.f_series_values.append(self.calculate_series(x))
            self.f_math_values.append(self.calculate_math_function(x))
            x += self.x_step

    def calculate_statistics(self, data: list, name: str) -> dict:
        """
        Расчет статистических характеристик последовательности
        
        Args:
            data: последовательность чисел
            name: название последовательности
        
        Returns:
            словарь со статистическими характеристиками
        """
        if not data:
            return {}
        
        n = len(data)
        
        # Среднее арифметическое
        mean = sum(data) / n
        
        # Медиана
        sorted_data = sorted(data)
        if n % 2 == 0:
            median = (sorted_data[n//2 - 1] + sorted_data[n//2]) / 2
        else:
            median = sorted_data[n//2]
        
        # Мода 
        counter = Counter(data)
        max_count = max(counter.values())
        modes = [value for value, count in counter.items() if count == max_count]
        mode = modes[0] if modes else None
        
        # Дисперсия
        variance = sum((x - mean) ** 2 for x in data) / n
        
        # Среднеквадратическое отклонение (СКО)
        std_deviation = math.sqrt(variance)
        
        return {
            'name': name,
            'count': n,
            'mean': round(mean, 6),
            'median': round(median, 6),
            'mode': round(mode, 6) if mode is not None else None,
            'variance': round(variance, 6),
            'std_deviation': round(std_deviation, 6),
            'min': round(min(data), 6),
            'max': round(max(data), 6)
        }
 
    def calculate_all_statistics(self) -> None:
        """Расчет статистики для всех последовательностей"""
        self.results['series_stats'] = self.calculate_statistics(self.f_series_values, 'Ряд')
        self.results['math_stats'] = self.calculate_statistics(self.f_math_values, 'Math')
        
        differences = [abs(s - m) for s, m in zip(self.f_series_values, self.f_math_values)]
        self.results['difference_stats'] = self.calculate_statistics(differences, '|Ряд - Math|')

    def plot_graphs(self, save_filename: str = "Task3/data/function_graph.png") -> None:
        """
        Построение графиков функций
        
        Args:
            save_filename: имя файла для сохранения графика
        """
        fig, ax = plt.subplots(figsize=(12, 8))
        
        line1, = ax.plot(self.x_values, self.f_series_values, 
                         'b-', linewidth=2, label=f'Разложение в ряд (n={self.n_terms})')

        x = np.arange(self.x_start, self.x_end, 0.01)
        y = np.log(1-x)
        line2, = ax.plot(x, y, 'r', linewidth=2, label=f'ln(1-x)')
        
        ax.axhline(y=0, color='k', linewidth=0.5, linestyle='-') 
        ax.axvline(x=0, color='k', linewidth=0.5, linestyle='-')  
        
        ax.grid(True, alpha=0.3, linestyle='--')
        
        ax.set_xlabel('x', fontsize=12, fontweight='bold')
        ax.set_ylabel('F(x)', fontsize=12, fontweight='bold')
        
        ax.set_title('Сравнение разложения функции в ряд и стандартной функции', 
                    fontsize=14, fontweight='bold')
        
        ax.legend(loc='best', fontsize=11, framealpha=0.9)
        
        ax.tick_params(axis='both', which='major', labelsize=10)
        
        annotation_text = f'Параметры:\nx ∈ [{self.x_start}, {self.x_end}]\nшаг = {self.x_step}\nколичество членов ряда = {self.n_terms}'
        ax.annotate(annotation_text, xy=(0.02, 0.98), xycoords='axes fraction',
                   fontsize=10, verticalalignment='top',
                   bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        max_diff_idx = np.argmax(np.abs(np.array(self.f_series_values) - np.array(self.f_math_values)))
        max_diff_x = self.x_values[max_diff_idx]
        max_diff_y_series = self.f_series_values[max_diff_idx]
        max_diff_y_math = self.f_math_values[max_diff_idx]
        
        ax.annotate(f'Макс. расхождение\nx={max_diff_x:.3f}\nΔ={abs(max_diff_y_series - max_diff_y_math):.4f}',
                   xy=(max_diff_x, (max_diff_y_series + max_diff_y_math)/2),
                   xytext=(max_diff_x + (self.x_end - self.x_start)*0.1, 
                          (max_diff_y_series + max_diff_y_math)/2 + 0.5),
                   arrowprops=dict(arrowstyle='->', color='gray', lw=1),
                   fontsize=9, bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.7))
        
        if 'difference_stats' in self.results:
            stats_text = (f'Статистика расхождения:\n'
                         f'среднее = {self.results["difference_stats"]["mean"]:.6f}\n'
                         f'СКО = {self.results["difference_stats"]["std_deviation"]:.6f}')
            ax.text(0.98, 0.5, stats_text, transform=ax.transAxes,
                   fontsize=9, verticalalignment='center', horizontalalignment='right',
                   bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
        
        plt.tight_layout()
        plt.savefig(save_filename, dpi=300, bbox_inches='tight')
        print(f"\nГрафик сохранен в файл '{save_filename}'")
        
        plt.show()

    def print_statistics(self) -> None:
        """Вывод статистических характеристик на экран"""
        print("\n" + "="*80)
        print("СТАТИСТИЧЕСКИЕ ХАРАКТЕРИСТИКИ ПОСЛЕДОВАТЕЛЬНОСТЕЙ")
        print("="*80)
        
        for stats in [self.results.get('series_stats'), 
                      self.results.get('math_stats'),
                      self.results.get('difference_stats')]:
            if not stats:
                continue
                
            print(f"\n{stats['name']}:")
            print(f"  Количество элементов: {stats['count']}")
            print(f"  Среднее арифметическое: {stats['mean']}")
            print(f"  Медиана: {stats['median']}")
            print(f"  Мода: {stats['mode']}")
            print(f"  Дисперсия: {stats['variance']}")
            print(f"  Среднеквадратическое отклонение: {stats['std_deviation']}")
            print(f"  Минимум: {stats['min']}")
            print(f"  Максимум: {stats['max']}")
    
    def save_statistics_to_file(self, filename: str = "Task3/data/statistics.txt") -> None:
        """Сохранение статистики в файл"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("СТАТИСТИЧЕСКИЕ ХАРАКТЕРИСТИКИ ПОСЛЕДОВАТЕЛЬНОСТЕЙ\n")
            f.write("="*80 + "\n\n")
            
            for stats in [self.results.get('series_stats'), 
                          self.results.get('math_stats'),
                          self.results.get('difference_stats')]:
                if not stats:
                    continue
                    
                f.write(f"\n{stats['name']}:\n")
                f.write(f"  Количество элементов: {stats['count']}\n")
                f.write(f"  Среднее арифметическое: {stats['mean']}\n")
                f.write(f"  Медиана: {stats['median']}\n")
                f.write(f"  Мода: {stats['mode']}\n")
                f.write(f"  Дисперсия: {stats['variance']}\n")
                f.write(f"  Среднеквадратическое отклонение: {stats['std_deviation']}\n")
                f.write(f"  Минимум: {stats['min']}\n")
                f.write(f"  Максимум: {stats['max']}\n")
        
        print(f"\nСтатистика сохранена в файл '{filename}'")

    def create_table(self) -> None:
        """Создание и вывод таблицы значений"""
        print("\n" + "="*80)
        print("ТАБЛИЦА ЗНАЧЕНИЙ")
        print("="*80)
        print(f"{'x':>10} | {'F(x) ряд':>15} | {'Math F(x)':>15} | {'Погрешность':>15}")
        print("-"*80)
        
        for i in range(len(self.x_values)):
            error = abs(self.f_series_values[i] - self.f_math_values[i])
            print(f"{self.x_values[i]:>10.4f} | {self.f_series_values[i]:>15.6f} | "
                  f"{self.f_math_values[i]:>15.6f} | {error:>15.6e}")

    def save_table_to_file(self, filename: str = "Task3/data/results_table.txt") -> None:
        """Сохранение таблицы значений в файл"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("ТАБЛИЦА ЗНАЧЕНИЙ\n")
            f.write("="*80 + "\n")
            f.write(f"{'x':>10} | {'F(x) ряд':>15} | {'Math F(x)':>15} | {'Погрешность':>15}\n")
            f.write("-"*80 + "\n")
            
            for i in range(len(self.x_values)):
                error = abs(self.f_series_values[i] - self.f_math_values[i])
                f.write(f"{self.x_values[i]:>10.4f} | {self.f_series_values[i]:>15.6f} | "
                       f"{self.f_math_values[i]:>15.6f} | {error:>15.6e}\n")
        
        print(f"\nТаблица сохранена в файл '{filename}'")

    def calculate_series(self, x: float, eps: float = 1e-5) -> float:
        """ln(1+x) = x - x²/2 + x³/3 - x⁴/4 + ..."""

        result: float = 0.0
        n: int = 1       
        ln2: float = math.log(2)   # iteration counter

        arg: float = 1 - x         # ln argument

        if arg < 0.0: 
            raise ValueError("ln arg less than 0")

        while arg >= 2.0:      
            arg /= 2.0
            result += ln2

        adder: float = 1 - arg           # var that adding to result
        while n < self.n_terms and abs(adder) >= eps:
            adder = pow(1 - arg, n) / float(n)
            result -= adder
            n += 1

        return result

    def calculate_math_function(self, x: float) -> float:
        return math.log(1 - x)

    def run(self) -> None:
        """Запуск полного анализа"""
        print("\n" + "="*80)
        print("АНАЛИЗ РАЗЛОЖЕНИЯ ФУНКЦИИ В РЯД")
        print("="*80)
        print(f"Параметры:\n  x от {self.x_start} до {self.x_end} с шагом {self.x_step}")
        print(f"  Количество членов ряда: {self.n_terms}")
        
        self.generate_data()
        
        self.create_table()
        self.save_table_to_file()
        
        self.calculate_all_statistics()
        
        self.print_statistics()
        self.save_statistics_to_file()
        
        self.plot_graphs()


def main():
    X_START = -0.8      
    X_END = 0.8         
    X_STEP = 0.2        
    N_TERMS = 500        
    
    analyzer = SeriesAnalyzer(X_START, X_END, X_STEP, N_TERMS)
    analyzer.run()


if __name__ == "__main__":
    main()