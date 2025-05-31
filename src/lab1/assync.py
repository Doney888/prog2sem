import asyncio


async def first_function():
    print("Функция 1: Первый print")
    await asyncio.sleep(1)
    print("Функция 1: Второй print")
    await asyncio.sleep(4)
    print("Функция 1: Третий print")


async def second_function():
    print("Функция 2: Первый print")
    await asyncio.sleep(3)
    print("Функция 2: Второй print")
    await asyncio.sleep(1)
    print("Функция 2: Третий print")
    await asyncio.sleep(1)
    print("Функция 2: Четвертый print")


async def main():
    task1 = asyncio.create_task(first_function())
    task2 = asyncio.create_task(second_function())

    await task1
    await task2

asyncio.run(main())