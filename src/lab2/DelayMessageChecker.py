from DelayMessage import delay_message
import asyncio

async def main():
    """Основная функция для демонстрации параллельного выполнения задач."""
    print("Запуск всех задач одновременно...")
    task1 = delay_message("Сообщение после 2 секунд", 2)
    task2 = delay_message("Сообщение после 1 секунды", 1)
    task3 = delay_message("Сообщение после 3 секунд", 3)
    await asyncio.gather(task1, task2, task3)

    print("Все задачи завершены!")

if __name__ == "__main__":
    asyncio.run(main())