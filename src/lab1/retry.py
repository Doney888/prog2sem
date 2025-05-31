import time
import functools


def retry(attempts=None, delay=1, exceptions=None):
    """
    Декоратор для повторных попыток вызова функции в случае ошибки.

    Параметры:
    attempts (int): Количество попыток вызова функции. Если None, то повторение до успеха.
    delay (int, float): Задержка между попытками в секундах. По умолчанию 1 секунда.
    exceptions (list): Список исключений, при которых будет повторяться попытка. Если None, то любое исключение.

    Возвращает:
    function: Функция, которая будет повторяться в случае ошибок.
    """
    if exceptions is None:
        exceptions = Exception  # Если не передан список исключений, использовать все исключения.

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            """
            Обёртка для функции, которая пытается вызвать её несколько раз
            в случае возникновения исключения из списка exceptions.
            """
            last_exception = None
            attempt = 0
            while attempt != attempts:
                try:
                    return func(*args, **kwargs)  # Попытка вызвать функцию
                except exceptions as e:
                    last_exception = e
                    print(f"Попытка {attempt + 1} не удалась: {e}")
                    if attempts is None or attempt < attempts - 1:  # Если ещё есть попытки
                        print(f"Повторная попытка через {delay} секунд...")
                        time.sleep(delay)  # Задержка перед повторной попыткой
                attempt += 1
            # Если все попытки неудачны, выбрасываем последнее исключение
            raise last_exception

        return wrapper

    return decorator
