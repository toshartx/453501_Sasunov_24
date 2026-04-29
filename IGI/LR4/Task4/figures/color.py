class FigureColor:
    """Класс для хранения цвета геометрической фигуры"""
    
    def __init__(self, color: str):
        self._color = color
    
    @property
    def color(self) -> str:
        """Свойство для получения цвета"""
        return self._color
    
    @color.setter
    def color(self, value: str) -> None:
        """Свойство для установки цвета"""
        self._color = value
    
    def __str__(self) -> str:
        return self._color