import importlib
import sys

def show_menu():
    print(f"{40 * '='} Лабораторная работа №4 {40 * '='}")
    print("Введите номер задания:")
    print("1 - Работа с университетом.")
    print("2 - Работа с текстом. Сбор статистики по тексту.")
    print("3 - Работа с matplotlib. График функции ln(1-x) + статистика по последовательности.")
    print("4 - Работа с фигурами. Отрисовка равнобедренной трапеции с заданными параметрами.")
    print("5 - Работа с numpy. Обмен позициями между наибольшими значениями первого и последнего столбцов,\nвычисление коэффицента корреляции.")
    print("6 - Работа с pandas. Получение информации о супермаркете.")
    print(100 * '-')
    print('0 - Завершение программы.')

def run_module(module_path):
    try:
        module = importlib.import_module(module_path)
        
        # Проверяем наличие функции main()
        if hasattr(module, 'main'):
            print('\n', 5 * '>')
            result = module.main()
            print(5 * '>')
        else:
            print(f"Ошибка: В модуле {module_path} нет функции main()")
            
    except ImportError as e:
        print(f"Ошибка импорта модуля {module_path}: {e}")
    except Exception as e:
        print(f"Ошибка при выполнении: {e}")
    
    input("\nНажмите Enter для продолжения...")

def main():
    modules = {
        1: 'Task1.University',
        2: 'Task2.TextAnalyzer',
        3: 'Task3.MathMethods',
        4: 'Task4.main',
        5: 'Task5.main',
        6: 'Task6.main'
    }

    while True:
        show_menu()

        try:
            choice = input("Ваш выбор: ").strip()
            
            if choice == '0':
                print("До свидания!")
                sys.exit(0)
            
            if choice.isdigit():
                choice_num = int(choice)
                if choice_num in modules:
                    module_path = modules[choice_num]
                    run_module(module_path)
                else:
                    print("Неверный выбор. Пожалуйста, выберите от 0 до 6")
            else:
                print("Пожалуйста, введите число")
        except KeyboardInterrupt:
            print("\n\nПрограмма прервана пользователем")
            sys.exit(0)
        except Exception as e:
            print(f"Произошла ошибка: {e}")
    

if __name__ == '__main__':
    main()
