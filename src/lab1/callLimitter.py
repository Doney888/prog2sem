import functools


def call_limiter(limit):
    """
    Декоратор для класса, который ограничивает количество вызовов каждого метода.

    Параметры:
    limit (int): Максимальное количество вызовов каждого метода.

    Возвращает:
    class: Класс с ограничениями на количество вызовов методов.
    """

    def decorator(cls):
        # Создаем новый класс, наследующий от оригинального
        class WrappedClass(cls):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self._method_counts = {}  # Словарь для хранения счетчиков вызовов

            def __getattribute__(self, name):
                attr = super().__getattribute__(name)

                # Пропускаем специальные методы и не-callable атрибуты
                if not callable(attr) or name.startswith('__') and name.endswith('__'):
                    return attr

                # Создаем обертку для метода
                @functools.wraps(attr)
                def wrapped(*args, **kwargs):
                    if name not in self._method_counts:
                        self._method_counts[name] = 0

                    if self._method_counts[name] >= limit:
                        raise Exception(
                            f"Метод {cls.__name__}.{name} был вызван {limit} раз(а), "
                            "дальнейшие вызовы запрещены."
                        )

                    self._method_counts[name] += 1
                    return attr(*args, **kwargs)

                return wrapped

        return WrappedClass

    return decorator
