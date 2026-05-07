from Task4.figures.trapezoid import IsoscelesTrapezoid

def validate_positive(value: float, name: str) -> bool:
    """
    Проверка корректности вводимых данных
    
    Args:
        value: проверяемое значение
        name: название параметра для сообщения
    
    Returns:
        True если значение корректно
    """
    if value <= 0:
        print(f"Ошибка: {name} должно быть положительным числом!")
        return False
    return True


def validate_angle(angle: float) -> bool:
    """
    Проверка корректности угла
    
    Args:
        angle: угол в градусах
    
    Returns:
        True если угол корректен (0 < angle < 180)
    """
    if angle <= 0 or angle >= 180:
        print("Ошибка: угол должен быть в диапазоне (0°, 180°)!")
        return False
    return True


def validate_trapezoid(a: float, b: float, angle: float) -> bool:
    """
    Проверка существования трапеции с заданными параметрами
    
    Условия:
    1. c = a - 2*b*cos(angle) > 0 (верхнее основание положительно)
    2. cos(angle) должен быть меньше a/(2*b)
    """
    import math
    angle_rad = math.radians(angle)
    cos_angle = math.cos(angle_rad)
    
    # Верхнее основание должно быть положительным
    top_base = a - 2 * b * cos_angle
    
    if top_base <= 0:
        print(f"Ошибка: Верхнее основание (c = {top_base:.2f}) должно быть положительным!")
        print(f"Проверьте, что a > 2*b*cos(α), т.е. {a:.2f} > {2*b*abs(cos_angle):.2f}")
        return False
    
    return True


def get_user_input():
    """Ввод значений параметров пользователем"""
    print("\n" + "="*60)
    print("ПОСТРОЕНИЕ РАВНОБЕДРЕННОЙ ТРАПЕЦИИ")
    print("="*60)
    
    # Ввод нижнего основания
    while True:
        try:
            a = float(input("\nВведите длину нижнего основания (a) > 0: "))
            if validate_positive(a, "Нижнее основание"):
                break
        except ValueError:
            print("Ошибка: Введите число!")
    
    # Ввод боковой стороны
    while True:
        try:
            b = float(input("Введите длину боковой стороны (b) > 0: "))
            if validate_positive(b, "Боковая сторона"):
                break
        except ValueError:
            print("Ошибка: Введите число!")
    
    # Ввод угла
    while True:
        try:
            angle = float(input("Введите угол между основанием и боковой стороной (0° < α < 180°): "))
            if validate_angle(angle):
                break
        except ValueError:
            print("Ошибка: Введите число!")
    
    # Проверка существования трапеции
    if not validate_trapezoid(a, b, angle):
        print("\nНевозможно построить трапецию с заданными параметрами!")
        print("Рекомендации: уменьшите угол или увеличьте основание a")
        return None
    
    # Ввод цвета
    color = input("Введите цвет фигуры (например: blue, red, green, yellow): ")
    
    # Ввод текста для подписи
    text_label = input("Введите текст для подписи фигуры (Enter для пропуска): ")
    if not text_label:
        text_label = None
    
    return {
        'a': a,
        'b': b,
        'angle': angle,
        'color': color,
        'text_label': text_label
    }


def main():
    """Основная функция для тестирования"""
    print("\n" + "="*60)
    print("ЗАДАНИЕ 4: ГЕОМЕТРИЧЕСКИЕ ФИГУРЫ")
    print("="*60)
    
    # Получение данных от пользователя
    params = get_user_input()
    
    if params is None:
        print("\nПрограмма завершена из-за ошибки ввода.")
        return
    
    # Создание объекта трапеции
    trapezoid = IsoscelesTrapezoid(
        a=params['a'],
        b=params['b'],
        angle=params['angle'],
    )

    trapezoid.color = params['color']
    
    # Вывод параметров фигуры
    print("\n" + "="*60)
    print("ПАРАМЕТРЫ ФИГУРЫ")
    print("="*60)
    print(trapezoid)
    
    # Построение и отображение фигуры
    print("\n" + "="*60)
    print("ПОСТРОЕНИЕ ФИГУРЫ")
    print("="*60)
    
    trapezoid.draw(
        text_label=params['text_label'],
        save_filename="Task4/data/trapezoid.png"
    )
    
    print("\n" + "="*60)
    print("ЗАВЕРШЕНИЕ РАБОТЫ")
    print("="*60)


if __name__ == "__main__":
    main()