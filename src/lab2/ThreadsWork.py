import time
import threading

def print_message(message, delay):
    """
    Функция для вывода сообщения с задержкой синхронно
    :param message: сообщение для вывода
    :param delay: задержка в секундах
    :return: None
    """
    time.sleep(delay)
    print(message)

def main():
    delay = 1
    messages = ["Сообщение 1", "Сообщение 2", "Сообщение 3"]

    start_time = time.time()
    for msg in messages:
        print_message(msg, delay)
    seq_time = time.time() - start_time
    print(f"Последовательное выполнение: {seq_time:.4f} сек\n")

    start_time = time.time()
    threads = []
    for msg in messages:
        t = threading.Thread(target=print_message, args=(msg, delay))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
    par_time = time.time() - start_time
    print(f"Параллельное выполнение: {par_time:.4f} сек")


if __name__ == "__main__":
    main()