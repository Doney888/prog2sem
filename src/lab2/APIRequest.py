import requests
import time
import aiohttp
import asyncio


def fetch_sync(url):
    """
    Функция для обращения к сайту синхронно
    :param url: ссылка на ресурс
    :return: время ответа ресурса
    """
    start = time.time()
    response = requests.get(url)
    elapsed = time.time() - start
    return f"{url} - {response.status_code} - {elapsed:.2f} сек"

async def fetch_async(session, url):
    """
    Функция для обращения к сайту асинхронно
    :param session: параметр, представляющий собой объект асинхронной HTTP-сессии
    :param url: ссылка на ресурс
    :return: время ответа ресурса
    """
    start = time.time()
    async with session.get(url) as response:
        await response.text()
        elapsed = time.time() - start
        return f"{url} - {response.status} - {elapsed:.2f} сек"

def main_sync():
    """
    Основная функция для синхронной части задания
    """
    urls = [
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/5",
        "https://httpbin.org/delay/10"
    ]

    start_time = time.time()

    print("Синхронные запросы:")
    for url in urls:
        print(fetch_sync(url))

    total_time = time.time() - start_time
    print(f"Общее время: {total_time:.2f} сек")

async def main_async():
    """
    Основная функция для асинхронной части задания
    """
    urls = [
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/5",
        "https://httpbin.org/delay/10"
    ]

    start_time = time.time()
    print("Асинхронные запросы:")

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_async(session, url) for url in urls]
        results = await asyncio.gather(*tasks)

        for result in results:
            print(result)

    total_time = time.time() - start_time
    print(f"Общее время: {total_time:.2f} сек")

if __name__ == "__main__":
    asyncio.run(main_async())