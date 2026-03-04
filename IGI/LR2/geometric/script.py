#!/usr/bin/env python3
import configparser
import os
import sys

# Добавляем путь к библиотеке geometric_lib
sys.path.append(os.path.join(os.path.dirname(__file__), 'geometric_lib'))

# Импортируем функции
from circle import area as circle_area, perimeter as circle_perimeter
from square import area as square_area, perimeter as square_perimeter

print("=" * 40)
print("Геометрические вычисления")
print("=" * 40)

# Читаем конфигурационный файл
config = configparser.ConfigParser()
config_path = os.path.join(os.path.dirname(__file__), 'config', 'config.ini')
config.read(config_path)

# Круг
if 'circle' in config:
    radius = float(config['circle']['radius'])
    print(f"\nКруг (радиус = {radius}):")
    print(f"  Площадь: {circle_area(radius):.2f}")
    print(f"  Периметр: {circle_perimeter(radius):.2f}")

# Прямоугольник
if 'rectangle' in config:
    a = float(config['rectangle']['side_a'])
    b = float(config['rectangle']['side_b'])
    print(f"\nПрямоугольник (стороны {a} и {b}):")
    print(f"  Площадь: {a * b:.2f}")
    print(f"  Периметр: {2 * (a + b):.2f}")

# Квадрат
if 'square' in config:
    side = float(config['square']['side'])
    print(f"\nКвадрат (сторона = {side}):")
    print(f"  Площадь: {square_area(side):.2f}")
    print(f"  Периметр: {square_perimeter(side):.2f}")

print("\n" + "=" * 40)