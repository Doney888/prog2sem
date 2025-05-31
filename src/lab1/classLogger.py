import time
import functools


def class_logger(show_magic_methods=True):
    """
    Декоратор класса, который логирует вызовы методов.

    Параметры:
    show_magic_methods (bool): Если True, логирует магические методы. По умолчанию True.

    Возвращает:
    class: Модифицированный класс с логированием вызовов методов.
    """

    def decorator(cls):
        class Wrapped(cls):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self._class_name = cls.__name__

            def __getattribute__(self, name):
                attr = super().__getattribute__(name)

                # Пропускаем не-callable атрибуты
                if not callable(attr):
                    return attr

                # Пропускаем магические методы, если show_magic_methods=False
                if not show_magic_methods and name.startswith('__') and name.endswith('__'):
                    return attr

                # Создаем обертку для метода
                @functools.wraps(attr)
                def wrapped(*args, **kwargs):
                    start_time = time.time()

                    # Логируем вызов метода
                    print(f"Выполняется метод: {cls.__name__}.{name}")
                    if args or kwargs:
                        print(f"Аргументы: args={args}, kwargs={kwargs}")

                    # Вызываем оригинальный метод
                    result = attr(*args, **kwargs)

                    # Логируем результат и время выполнения
                    execution_time = time.time() - start_time
                    print(f"Результат: {result}")
                    print(f"Время выполнения: {execution_time:.4f} сек")

                    return result

                return wrapped

        return Wrapped

    return decorator
