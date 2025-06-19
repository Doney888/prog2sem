import asyncio

async def delay_message(message: str, delay: float):
    """
    Функция для вывода сообщения с задержкой асинхронно
    :param message: сообщение для вывода
    :param delay: задержка между вызовом функции и выводом сообщения
    :return: сообщение из параметра message
    """
    await asyncio.sleep(delay)
    print(message)