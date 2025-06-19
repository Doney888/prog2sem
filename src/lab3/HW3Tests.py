import os
import sys
import stat
import time
import tempfile
import unittest
import platform
from unittest.mock import patch, MagicMock

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

class TestAssignment1(unittest.TestCase):
    """Тесты для Задания 1"""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        os.chdir(self.test_dir)
        self.script_path = os.path.join(self.test_dir, "task1.py")

        self.test_file = os.path.join(self.test_dir, "test_file.txt")
        with open(self.test_file, 'w') as f:
            f.write("Test content")

    def tearDown(self):
        for root, dirs, files in os.walk(self.test_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(self.test_dir)

    def test_file_creation(self):
        """Проверка создания файла"""
        # Создаем файл
        test_file = "new_file.txt"
        with open(test_file, 'w') as f:
            f.write("Test")

        self.assertTrue(os.path.exists(test_file))

    def test_file_metadata(self):
        """Проверка метаданных файла"""
        file_stats = os.stat(self.test_file)

        self.assertGreater(file_stats.st_size, 0)

        self.assertLess(file_stats.st_mtime, time.time())
        self.assertLess(file_stats.st_atime, time.time())

    def test_permission_changes(self):
        """Проверка изменения прав доступа"""
        original_mode = os.stat(self.test_file).st_mode

        new_permissions = original_mode | stat.S_IEXEC
        os.chmod(self.test_file, new_permissions)

        updated_mode = os.stat(self.test_file).st_mode
        self.assertEqual(updated_mode & stat.S_IEXEC, stat.S_IEXEC)

    def test_current_user(self):
        """Проверка получения текущего пользователя"""
        username = os.getlogin() if hasattr(os, 'getlogin') else os.environ.get('USER', os.environ.get('USERNAME', ''))
        self.assertTrue(username.strip() != "")


class TestAssignment2(unittest.TestCase):
    """Тесты для Задания 2"""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        os.chdir(self.test_dir)

        self.file1 = os.path.join(self.test_dir, "file1.txt")
        with open(self.file1, 'w') as f:
            f.write("File 1 content")

        self.subdir = os.path.join(self.test_dir, "subdir")
        os.makedirs(self.subdir)

        self.file2 = os.path.join(self.subdir, "file2.txt")
        with open(self.file2, 'w') as f:
            f.write("File 2 content")

    def tearDown(self):
        for root, dirs, files in os.walk(self.test_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(self.test_dir)

    def test_directory_creation(self):
        """Проверка создания директорий"""
        new_dir = os.path.join(self.test_dir, "new_directory")
        os.makedirs(new_dir)
        self.assertTrue(os.path.isdir(new_dir))

    def test_file_copy(self):
        """Проверка копирования файла"""
        copy_path = os.path.join(self.test_dir, "file1_copy.txt")

        with open(self.file1, 'r') as src, open(copy_path, 'w') as dst:
            dst.write(src.read())

        self.assertTrue(os.path.exists(copy_path))
        with open(copy_path, 'r') as f:
            content = f.read()
        self.assertEqual(content, "File 1 content")

    def test_file_rename(self):
        """Проверка переименования файла"""
        new_path = os.path.join(self.test_dir, "renamed.txt")
        os.rename(self.file1, new_path)
        self.assertTrue(os.path.exists(new_path))
        self.assertFalse(os.path.exists(self.file1))

    def test_file_move(self):
        """Проверка перемещения файла"""
        new_path = os.path.join(self.subdir, "moved.txt")
        os.rename(self.file1, new_path)
        self.assertTrue(os.path.exists(new_path))
        self.assertFalse(os.path.exists(self.file1))

    def test_directory_listing(self):
        """Проверка листинга директорий"""
        root_items = os.listdir(self.test_dir)
        self.assertIn("file1.txt", root_items)
        self.assertIn("subdir", root_items)

        subdir_items = os.listdir(self.subdir)
        self.assertIn("file2.txt", subdir_items)

    def test_directory_walk(self):
        """Проверка обхода директорий"""
        with open(os.path.join(self.subdir, "file3.txt"), 'w') as f:
            f.write("File 3")

        found = []
        for root, dirs, files in os.walk(self.test_dir):
            rel_path = os.path.relpath(root, self.test_dir)
            found.append((rel_path, sorted(dirs), sorted(files)))

        expected = [
            ('.', ['subdir'], ['file1.txt']),
            ('subdir', [], ['file2.txt', 'file3.txt'])
        ]

        self.assertEqual(found, expected)

    def test_directory_operations(self):
        """Проверка создания и удаления директорий"""
        new_dir = os.path.join(self.test_dir, "temp_dir")
        os.makedirs(new_dir)
        self.assertTrue(os.path.exists(new_dir))

        os.rmdir(new_dir)
        self.assertFalse(os.path.exists(new_dir))


class TestAssignment3(unittest.TestCase):
    """Тесты для Задания 3"""

    @patch('psutil.process_iter')
    def test_show_running_processes(self, mock_process_iter):
        """Проверка отображения запущенных процессов"""
        mock_proc1 = MagicMock()
        mock_proc1.info = {
            'pid': 123,
            'name': 'test_process1',
            'username': 'user1',
            'create_time': time.time() - 3600
        }

        mock_proc2 = MagicMock()
        mock_proc2.info = {
            'pid': 456,
            'name': 'test_process2',
            'username': 'user2',
            'create_time': time.time() - 7200
        }

        mock_process_iter.return_value = [mock_proc1, mock_proc2]

        from SysWorks import show_running_processes
        show_running_processes()

    @patch('psutil.Process')
    def test_show_process_details(self, mock_process):
        """Проверка отображения деталей процесса"""
        # Настраиваем мок-процесс
        mock_proc = MagicMock()
        mock_proc.name.return_value = "test_process"
        mock_proc.status.return_value = "running"
        mock_proc.username.return_value = "testuser"
        mock_proc.create_time.return_value = time.time() - 3600
        mock_proc.cpu_percent.return_value = 12.5
        mock_proc.memory_info.return_value.rss = 1024 * 1024 * 10  # 10 MB
        mock_proc.cmdline.return_value = ["test", "--arg"]
        mock_proc.cwd.return_value = "/test/dir"

        mock_process.return_value = mock_proc

        from SysWorks import show_process_details
        with patch('builtins.input', return_value="123"):
            show_process_details()

    @patch('psutil.Process')
    @patch('builtins.input')
    def test_terminate_process(self, mock_input, mock_process):
        """Проверка завершения процесса"""
        mock_proc = MagicMock()
        mock_process.return_value = mock_proc
        mock_input.side_effect = ["123", "y"]

        from SysWorks import terminate_process
        terminate_process()

        mock_proc.terminate.assert_called_once()

    def test_environment_variables(self):
        """Проверка работы с переменными окружения"""
        original_env = os.environ.copy()

        try:
            from SysWorks import manage_environment_variables

            with patch('builtins.input', return_value="3"):
                manage_environment_variables()

            with patch('builtins.input', side_effect=["1", "TEST_VAR", "TEST_VALUE", "3"]):
                manage_environment_variables()
                self.assertEqual(os.environ["TEST_VAR"], "TEST_VALUE")

            with patch('builtins.input', side_effect=["2", "3"]):
                manage_environment_variables()

        finally:
            os.environ.clear()
            os.environ.update(original_env)

    @patch('psutil.Process')
    @patch('builtins.input')
    def test_change_process_priority(self, mock_input, mock_process):
        """Проверка изменения приоритета процесса"""
        mock_proc = MagicMock()
        mock_process.return_value = mock_proc
        mock_input.side_effect = ["123", "2"]

        from SysWorks import change_process_priority
        change_process_priority()

        mock_proc.nice.assert_called_with(2)

    @patch('platform.system')
    @patch('platform.release')
    @patch('platform.version')
    @patch('platform.machine')
    @patch('platform.processor')
    @patch('psutil.virtual_memory')
    @patch('psutil.disk_usage')
    @patch('psutil.cpu_percent')
    def test_show_system_info(self, mock_cpu, mock_disk, mock_mem,
                              mock_processor, mock_machine,
                              mock_version, mock_release, mock_system):
        """Проверка отображения системной информации"""
        mock_system.return_value = "TestOS"
        mock_release.return_value = "1.0"
        mock_version.return_value = "Test Version"
        mock_machine.return_value = "x86_64"
        mock_processor.return_value = "Test CPU"

        mem_mock = MagicMock()
        mem_mock.total = 1024 ** 3 * 8  # 8 GB
        mem_mock.available = 1024 ** 3 * 2  # 2 GB
        mock_mem.return_value = mem_mock

        disk_mock = MagicMock()
        disk_mock.total = 1024 ** 3 * 100  # 100 GB
        disk_mock.free = 1024 ** 3 * 30  # 30 GB
        mock_disk.return_value = disk_mock

        mock_cpu.return_value = 25.5

        from SysWorks import show_system_info
        show_system_info()


if __name__ == "__main__":
    print("Запуск модульных тестов...")
    print(f"Платформа: {platform.system()} {platform.release()}")
    print(f"Python: {sys.version}")

    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"\nСоздана временная директория: {temp_dir}")
        os.chdir(temp_dir)

        unittest.main(exit=False)

    print("\nВсе тесты завершены!")