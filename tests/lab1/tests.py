from assync import *
from callLimitter import *
from classLogger import *
from retry import *
from logger import *
import unittest
from unittest.mock import patch
from io import StringIO


class TestLoggerDecorator(unittest.TestCase):

    def test_logger_prints_function_name(self):
        @logger
        def say_hello():
            return "Hello"

        with patch('sys.stdout', new=StringIO()) as fake_out:
            say_hello()
            output = fake_out.getvalue()
            self.assertIn("Выполняется функция: say_hello", output)

    def test_logger_prints_arguments(self):
        @logger
        def add(a, b):
            return a + b

        with patch('sys.stdout', new=StringIO()) as fake_out:
            add(2, 3)
            output = fake_out.getvalue()
            self.assertIn("Аргументы: (2, 3)", output)

    def test_logger_prints_result(self):
        @logger
        def multiply(x, y):
            return x * y

        with patch('sys.stdout', new=StringIO()) as fake_out:
            multiply(4, 5)
            output = fake_out.getvalue()
            self.assertIn("Результат: 20", output)


class TestRetryDecorator(unittest.TestCase):

    def test_retry_success_after_one_failure(self):
        attempts = []

        @retry(attempts=2, delay=0.1)
        def unstable_function():
            if len(attempts) < 1:
                attempts.append(1)
                raise ValueError("Ошибка")
            return "Успех"

        result = unstable_function()
        self.assertEqual(result, "Успех")
        self.assertEqual(len(attempts), 1)

    def test_retry_fails_after_all_attempts(self):
        @retry(attempts=3, delay=0.1, exceptions=RuntimeError)
        def always_failing():
            raise RuntimeError("Всегда ошибка")

        with self.assertRaises(RuntimeError):
            always_failing()


class TestClassLoggerDecorator(unittest.TestCase):

    def test_class_logger_prints_method_call(self):
        @class_logger(show_magic_methods=False)
        class Calculator:
            def add(self, a, b):
                return a + b

        with patch('sys.stdout', new=StringIO()) as fake_out:
            calc = Calculator()
            calc.add(10, 20)
            output = fake_out.getvalue()
            self.assertIn("Выполняется метод: Calculator.add", output)

    def test_class_logger_hides_magic_methods(self):
        @class_logger(show_magic_methods=False)
        class TestClass:
            def __str__(self):
                return "Объект"

        with patch('sys.stdout', new=StringIO()) as fake_out:
            obj = TestClass()
            str(obj)  # Этот вызов не должен логироваться
            output = fake_out.getvalue()
            self.assertEqual(output, "")  # Вывода быть не должно


class TestCallLimiterDecorator(unittest.TestCase):

    def test_call_limiter_allows_limited_calls(self):
        @call_limiter(limit=2)
        class Counter:
            def increment(self):
                return "OK"

        counter = Counter()
        self.assertEqual(counter.increment(), "OK")  # 1-й вызов
        self.assertEqual(counter.increment(), "OK")  # 2-й вызов

    def test_call_limiter_blocks_extra_calls(self):
        @call_limiter(limit=1)
        class OneTime:
            def perform(self):
                return "Сделано"

        obj = OneTime()
        obj.perform()  # 1-й вызов - разрешен

        with self.assertRaises(Exception) as error:
            obj.perform()  # 2-й вызов - должен вызвать ошибку

        self.assertIn("был вызван 1 раз(а)", str(error.exception))


if __name__ == "__main__":
    unittest.main()