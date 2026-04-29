from abc import ABC, abstractmethod
import math

class GeometricFigure(ABC):
    
    @abstractmethod
    def calculate_area(self) -> float:
        """Абстрактный метод вычисления площади фигуры"""
        pass
    
    @abstractmethod
    def get_parameters(self) -> str:
        """Абстрактный метод получения параметров фигуры"""
        pass