import os
import sys
import platform
import psutil
from datetime import datetime
import ctypes

if "TERM" not in os.environ:
    os.environ["TERM"] = "xterm"

def clear_screen():
    """Очистка экрана консоли с проверкой TERM"""
    try:
        if platform.system() == "Windows":
            os.system('cls')
        else:
            if os.environ.get("TERM", "") not in ["", "dumb"]:
                os.system('clear')
            else:
                print("\n" * 100)
    except Exception:
        pass

def show_running_processes():
    """Показать список всех запущенных процессов"""
    print("\n{:<8} {:<25} {:<15} {:<15}".format("PID", "Имя", "Пользователь", "Запущен"))
    print("-" * 65)

    for proc in psutil.process_iter(['pid', 'name', 'username', 'create_time']):
        try:
            create_time = datetime.fromtimestamp(proc.info['create_time']).strftime("%Y-%m-%d %H:%M")
            username = proc.info['username']
            if username:
                username = username.split('\\')[-1] if '\\' in username else username
                username = username[:14]
            else:
                username = "N/A"

            print("{:<8} {:<25} {:<15} {:<15}".format(
                proc.info['pid'],
                (proc.info['name'] or '')[0:24],
                username,
                create_time
            ))
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue


def show_process_details():
    """Показать детальную информацию о процессе по PID"""
    try:
        pid = int(input("\nВведите PID процесса: "))
        proc = psutil.Process(pid)

        print(f"\nДетальная информация о процессе (PID: {pid}):")
        print(f"Имя: {proc.name()}")
        print(f"Статус: {proc.status()}")
        print(f"Пользователь: {proc.username()}")
        print(f"Запущен: {datetime.fromtimestamp(proc.create_time()).strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Использует CPU: {proc.cpu_percent(interval=0.1):.1f}%")
        print(f"Использует памяти: {proc.memory_info().rss / (1024 * 1024):.2f} MB")

        try:
            print(f"Командная строка: {' '.join(proc.cmdline())}")
        except psutil.AccessDenied:
            print("Командная строка: недоступна (требуются права)")

        try:
            print(f"Рабочая директория: {proc.cwd()}")
        except (psutil.AccessDenied, FileNotFoundError):
            print("Рабочая директория: недоступна")

    except ValueError:
        print("Ошибка: Введите числовой PID")
    except psutil.NoSuchProcess:
        print("Ошибка: Процесс с таким PID не найден")
    except psutil.AccessDenied:
        print("Ошибка: Нет прав доступа к этому процессу")


def terminate_process():
    """Завершить процесс по PID"""
    try:
        pid = int(input("\nВведите PID процесса для завершения: "))
        proc = psutil.Process(pid)
        proc_name = proc.name()

        confirm = input(f"Вы уверены, что хотите завершить процесс '{proc_name}' (PID: {pid})? [y/n]: ")
        if confirm.lower() == 'y':
            try:
                proc.terminate()
                print(f"Процесс '{proc_name}' (PID: {pid}) успешно завершен")
            except psutil.AccessDenied:
                print("Ошибка: Нет прав для завершения этого процесса")
    except ValueError:
        print("Ошибка: Введите числовой PID")
    except psutil.NoSuchProcess:
        print("Ошибка: Процесс с таким PID не найден")


def manage_environment_variables():
    """Управление переменными окружения"""
    print("\nТекущие переменные окружения:")
    vars = list(os.environ.items())

    for key, value in vars[:10]:
        print(f"{key}={value}")

    if len(vars) > 10:
        print(f"... (показано 10 из {len(vars)}, используйте 'показать все' для полного списка)")

    action = input("\nВыберите действие: [1] Добавить переменную [2] Показать все [3] Назад: ")

    if action == '1':
        key = input("Введите имя переменной: ").strip()
        value = input("Введите значение: ").strip()
        if key and value:
            os.environ[key] = value
            print(f"Переменная {key} успешно добавлена (для текущей сессии)")
        else:
            print("Ошибка: Имя и значение не могут быть пустыми")
    elif action == '2':
        for key, value in vars:
            print(f"{key}={value}")


def change_process_priority():
    """Изменение приоритета процесса"""
    try:
        pid = int(input("\nВведите PID процесса: "))
        proc = psutil.Process(pid)

        print("\nТекущий приоритет процесса:")
        print(f"PID: {pid}, Имя: {proc.name()}, Приоритет: {proc.nice()}")

        print("\nДоступные уровни приоритета:")
        print("0 - Высокий (только для администраторов)")
        print("1 - Выше среднего")
        print("2 - Средний")
        print("3 - Ниже среднего")
        print("4 - Низкий")

        try:
            new_priority = int(input("Введите новый приоритет (0-4): "))
        except ValueError:
            print("Ошибка: Введите число от 0 до 4")
            return

        if 0 <= new_priority <= 4:
            try:
                proc.nice(new_priority)
                print(f"Приоритет процесса {pid} успешно изменен на {new_priority}")
            except psutil.AccessDenied:
                print("Ошибка: Нет прав для изменения приоритета процесса")
        else:
            print("Ошибка: Неверный уровень приоритета")
    except ValueError:
        print("Ошибка: Введите числовой PID")
    except psutil.NoSuchProcess:
        print("Ошибка: Процесс с таким PID не найден")


def show_system_info():
    """Показать информацию о системе"""
    print("\nИнформация о системе:")
    print(f"Операционная система: {platform.system()} {platform.release()}")
    print(f"Версия ОС: {platform.version()}")
    print(f"Архитектура: {platform.machine()}")

    try:
        print(f"Процессор: {platform.processor()}")
    except:
        print("Процессор: информация недоступна")

    # Информация о памяти
    try:
        mem = psutil.virtual_memory()
        print(f"\nПамять: Всего {mem.total / (1024 ** 3):.2f} GB, Доступно {mem.available / (1024 ** 3):.2f} GB")
    except:
        print("\nИнформация о памяти недоступна")

    # Информация о диске
    try:
        disk = psutil.disk_usage('/')
        print(f"Диск: Всего {disk.total / (1024 ** 3):.2f} GB, Свободно {disk.free / (1024 ** 3):.2f} GB")
    except:
        print("Информация о диске недоступна")

    # Загрузка CPU
    try:
        print(f"Загрузка CPU: {psutil.cpu_percent(interval=1)}%")
    except:
        print("Информация о CPU недоступна")


def main():
    """Главная функция с меню управления"""
    admin_warning = False
    if platform.system() == "Windows":
        try:
            admin_warning = ctypes.windll.shell32.IsUserAnAdmin() == 0
        except:
            admin_warning = True
    else:
        admin_warning = os.geteuid() != 0

    while True:
        print("\n" + "=" * 50)
        print("Системный монитор и менеджер процессов")
        print("=" * 50)
        if admin_warning:
            print("Внимание: Некоторые функции требуют прав администратора")
            print("=" * 50)
        print("a) Список запущенных процессов")
        print("b) Информация о процессе")
        print("c) Завершить процесс")
        print("d) Переменные окружения")
        print("e) Изменить приоритет процесса")
        print("f) Информация о системе")
        print("g) Выход")

        choice = input("\nВыберите действие: ").strip().lower()

        if choice == 'a':
            show_running_processes()
        elif choice == 'b':
            show_process_details()
        elif choice == 'c':
            terminate_process()
        elif choice == 'd':
            manage_environment_variables()
        elif choice == 'e':
            change_process_priority()
        elif choice == 'f':
            show_system_info()
        elif choice == 'g':
            print("Завершение работы...")
            sys.exit(0)
        else:
            print("Неверный выбор. Попробуйте снова.")

        input("\nНажмите Enter для продолжения...")
        clear_screen()


if __name__ == "__main__":
    main()