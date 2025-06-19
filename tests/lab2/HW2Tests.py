import unittest
from unittest.mock import patch, MagicMock, call

import DataRace
import DataRaceFixed
import ThreadsWork
from APIRequest import *
from DelayMessageChecker import *
from ThreadsWork import *

class TestAsyncFunctions(unittest.TestCase):
    """Тесты для заданий 1-2 (асинхронные функции)"""

    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def tearDown(self):
        self.loop.close()

    def test_delay_message(self):
        """Тест одиночного вывода сообщения с задержкой"""
        with patch("asyncio.sleep", new_callable=MagicMock) as mock_sleep:
            mock_sleep.return_value = asyncio.Future()
            mock_sleep.return_value.set_result(None)

            coro = delay_message("Test", 1.5)
            self.loop.run_until_complete(coro)

            mock_sleep.assert_called_once_with(1.5)

    def test_parallel_execution(self):
        """Тест параллельного выполнения задач"""
        with patch("asyncio.sleep", new_callable=MagicMock) as mock_sleep:
            mock_sleep.return_value = asyncio.Future()
            mock_sleep.return_value.set_result(None)

            tasks = [
                delay_message("Msg1", 0.3),
                delay_message("Msg2", 0.1),
                delay_message("Msg3", 0.2)
            ]

            self.loop.run_until_complete(asyncio.gather(*tasks))

            self.assertEqual(mock_sleep.call_count, 3)
            expected_calls = [call(0.3), call(0.1), call(0.2)]
            mock_sleep.assert_has_calls(expected_calls, any_order=True)


class TestHTTPRequests(unittest.TestCase):
    """Тесты для задания 3 (HTTP запросы)"""

    def test_sync_http_request(self):
        """Тест синхронного HTTP запроса"""
        with patch("requests.get") as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_get.return_value = mock_response

            result = fetch_sync("https://test.com")
            self.assertIn("https://test.com", result)
            self.assertIn("200", result)

    async def test_async_http_request(self):
        """Тест асинхронного HTTP запроса"""

        async def run_test():
            with patch("aiohttp.ClientSession") as mock_session:
                mock_response = MagicMock()
                mock_response.status = 200
                mock_session.return_value.__aenter__.return_value.get.return_value.__aenter__.return_value = mock_response

                async with aiohttp.ClientSession() as session:
                    result = await fetch_async(session, "https://test.com")
                    self.assertIn("https://test.com", result)
                    self.assertIn("200", result)

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(run_test())
        loop.close()


class TestThreads(unittest.TestCase):
    """Тесты для задания 4 (работа с потоками)"""

    @patch("time.sleep")
    @patch("builtins.print")
    def test_print_message(self, mock_print, mock_sleep):
        """Тест функции вывода сообщения"""
        ThreadsWork.print_message("Test", 0.1)
        mock_sleep.assert_called_once_with(0.1)
        mock_print.assert_called_once_with("Test")

    @patch.object(ThreadsWork, 'print_message')
    async def test_thread_execution_time(self, mock_print):
        """Тест времени выполнения потоков"""
        mock_print.side_effect = lambda msg, delay: time.sleep(delay)

        start_time = time.time()
        ThreadsWork.main()
        elapsed = time.time() - start_time

        self.assertAlmostEqual(elapsed, 1.0, delta=0.1)


class TestRaceCondition(unittest.TestCase):
    """Тесты для заданий 5-6 (гонка данных и блокировки)"""

    def setUp(self):
        DataRace.counter = 0
        DataRaceFixed.counter = 0

    async def test_unsafe_increment(self):
        """Тест небезопасного увеличения счетчика"""
        threads = []
        for _ in range(100):
            t = threading.Thread(target=DataRace.increment())
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        self.assertNotEqual(DataRace.counter, 100)
        print(f"Небезопасное значение: {DataRace.counter}")

    def test_safe_increment(self):
        """Тест безопасного увеличения счетчика с блокировкой"""
        threads = []
        for _ in range(100):
            t = threading.Thread(target=DataRaceFixed.safe_increment)
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        self.assertEqual(DataRaceFixed.counter, 100)

    def test_lock_mechanism(self):
        """Тест механизма блокировки"""
        lock = DataRaceFixed.lock
        self.assertFalse(lock.locked())

        with lock:
            self.assertTrue(lock.locked())

        self.assertFalse(lock.locked())


if __name__ == "__main__":
    unittest.main()