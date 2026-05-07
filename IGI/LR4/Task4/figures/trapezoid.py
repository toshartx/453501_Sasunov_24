import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Polygon
from abc import ABC, abstractmethod
from .abstract_figure import GeometricFigure
from .color import FigureColorMixin

class IsoscelesTrapezoid(GeometricFigure, FigureColorMixin):
    """
    Класс равнобедренной трапеции
    
    Параметры:
        a: нижнее основание
        b: боковая сторона
        angle: угол между основанием a и боковой стороной b (в градусах)
        color: цвет фигуры
    """
    
    # Поле данных класса (название фигуры)
    _figure_name = "Равнобедренная трапеция"
    
    def __init__(self, a: float, b: float, angle: float):
        self._a = a 
        self._b = b 
        self._angle = angle
        
        self._c = self._calculate_top_base()
        
        self._height = self._calculate_height()
        
        self._area = None
    
    def _calculate_top_base(self) -> float:
        """
        Вычисление верхнего основания трапеции
        c = a - 2 * b * cos(angle)
        """
        angle_rad = math.radians(self._angle)
        return self._a - 2 * self._b * math.cos(angle_rad)
    
    def _calculate_height(self) -> float:
        """
        Вычисление высоты трапеции
        h = b * sin(angle)
        """
        angle_rad = math.radians(self._angle)
        return self._b * math.sin(angle_rad)
    
    def calculate_area(self) -> float:
        """
        Вычисление площади трапеции
        S = (a + c) * h / 2
        """
        if self._area is None:
            self._area = (self._a + self._c) * self._height / 2
        return self._area
    
    @classmethod
    def get_figure_name(cls) -> str:
        """Возвращает название фигуры (метод класса)"""
        return cls._figure_name
    
    def get_parameters(self) -> str:
        """Возвращает основные параметры фигуры в виде строки"""
        return ("Название: {name}\n"
                "Нижнее основание (a): {a:.2f}\n"
                "Верхнее основание (c): {c:.2f}\n"
                "Боковая сторона (b): {b:.2f}\n"
                "Высота (h): {height:.2f}\n"
                "Угол между a и b: {angle:.1f}°\n"
                "Цвет: {color}\n"
                "Площадь: {area:.2f}".format(
                    name=self.get_figure_name(),
                    a=self._a,
                    c=self._c,
                    b=self._b,
                    height=self._height,
                    angle=self._angle,
                    color=self.color,
                    area=self.calculate_area()
                ))
    
    def __str__(self) -> str:
        """Строковое представление фигуры"""
        return self.get_parameters()
    
    def get_vertices(self):
        """
        Получение координат вершин трапеции для построения
        
        Возвращает список координат [(x1,y1), (x2,y2), (x3,y3), (x4,y4)]
        """
        x1, y1 = 0, 0
        x2, y2 = self._a, 0
        
        offset = (self._a - self._c) / 2
        x3, y3 = offset + self._c, self._height
        x4, y4 = offset, self._height
        
        return [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
    
    def draw(self, text_label: str = '', save_filename: str = "output/trapezoid.png"):
        """
        Построение и отображение фигуры
        
        Args:
            text_label: текст для подписи фигуры
            save_filename: имя файла для сохранения
        """
        fig, ax = plt.subplots(figsize=(10, 8))
        
        vertices = self.get_vertices()
        
        trapezoid = Polygon(vertices, closed=True, 
                           facecolor=self.color, 
                           edgecolor='black', 
                           linewidth=2,
                           alpha=0.7)
        ax.add_patch(trapezoid)
        
        ax.set_xlim(-1, self._a + 1)
        ax.set_ylim(-1, self._height + 1)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3, linestyle='--')
        
        ax.set_xlabel('X', fontsize=12)
        ax.set_ylabel('Y', fontsize=12)
        ax.set_title(f'{self.get_figure_name()}\n{self.get_parameters()}', 
                    fontsize=10, wrap=True)
        
        if text_label:
            center_x = self._a / 2
            center_y = self._height / 2
            ax.text(center_x, center_y, text_label, 
                   ha='center', va='center', 
                   fontsize=12, fontweight='bold',
                   bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        params_text = f"a = {self._a:.2f}\nb = {self._b:.2f}\nα = {self._angle:.1f}°\nS = {self.calculate_area():.2f}"
        ax.annotate(params_text, xy=(0.02, 0.98), xycoords='axes fraction',
                   fontsize=9, verticalalignment='top',
                   bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        ax.axhline(y=0, color='k', linewidth=0.5, linestyle='-')
        ax.axvline(x=0, color='k', linewidth=0.5, linestyle='-')
        
        plt.tight_layout()
        
        plt.savefig(save_filename, dpi=300, bbox_inches='tight')
        print(f"\nФигура сохранена в файл '{save_filename}'")
        
        plt.show()