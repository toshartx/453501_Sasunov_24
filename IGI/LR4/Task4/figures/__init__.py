"""Пакет с классами геометрических фигур"""

from .abstract_figure import GeometricFigure
from .color import FigureColor
from .trapezoid import IsoscelesTrapezoid

__all__ = ['GeometricFigure', 'FigureColor', 'IsoscelesTrapezoid']