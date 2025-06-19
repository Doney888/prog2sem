import threading
import time

counter = 0
lock = threading.Lock()

def safe_increment():
    """Функция имитирует работу функции и безопасно увеличивает глобальную переменную counter"""
    global counter
    with lock:
        current_value = counter
        time.sleep(0.001)
        counter = current_value + 1


def main():
    global counter
    num_threads = 100
    threads = []

    counter = 0

    for _ in range(num_threads):
        t = threading.Thread(target=safe_increment)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print(f"Ожидаемое значение: {num_threads}")
    print(f"Фактическое значение: {counter}")


if __name__ == "__main__":
    main()