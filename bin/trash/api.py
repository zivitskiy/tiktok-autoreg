import aiohttp
from config import *
import logging
import asyncio
import certifi
import ssl

BASE_URL = "https://5sim.biz/v1"

class Api():
    @staticmethod
    async def get_countries():
        headers = {
            "Authorization": f"Bearer {SIM5_API_KEY}",
            "Accept": "application/json"
        }
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context)) as session:
            async with session.get(f"{BASE_URL}/guest/countries", headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    countries = []
                    for country_code, country_data in data.items():
                        countries.append({
                            "code": country_code,
                            "name": country_data["text_ru"]
                        })
                    return countries
                elif response.status == 403:
                    logging.error(f"Ошибка получения стран: {response.status} — Доступ запрещён.")
                else:
                    logging.error(f"Ошибка получения стран: {response.status}")
                return []

    @staticmethod
    async def get_balance():
        headers = {
            "Authorization": f"Bearer {SIM5_API_KEY}",
            "Accept": "application/json"
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(f"{BASE_URL}/user/profile", headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("balance", 0)
                elif response.status == 403:
                    logging.error(f"Ошибка получения баланса: {response.status} — Доступ запрещён.")
                    return None
                else:
                    logging.error(f"Ошибка получения баланса: {response.status}")
                    return None

    @staticmethod
    async def get_info(country_code: str):
        headers = {
            "Accept": "application/json"
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(f"{BASE_URL}/guest/products/{country_code}/any", headers=headers) as response:
                if response.status == 200:
                    data = await response.json()

                    if isinstance(data, dict):
                        account_info = []
                        for product, details in data.items():
                            account_info.append({
                                "product": product,
                                "available": details.get("Qty", 0),
                                "price": details.get("Price", 0)
                            })
                        return account_info
                    else:
                        logging.error(f"Неверный формат ответа: {data}")
                        return None
                elif response.status == 403:
                    logging.error(f"Ошибка получения информации об аккаунтах: {response.status} — Доступ запрещён.")
                else:
                    logging.error(f"Ошибка получения информации об аккаунтах: {response.status}")
                return None

    @staticmethod
    async def buy(country_code: str):
        headers = {
            "Authorization": f"Bearer {SIM5_API_KEY}",
            "Accept": "application/json"
        }

        logging.info(f"Покупка номера для страны с кодом: {country_code}")

        async with aiohttp.ClientSession() as session:
            url = f"{BASE_URL}/user/buy/activation/{country_code}/any/tiktok"
            logging.info(f"URL запроса для покупки номера: {url}")
            async with session.get(url, headers=headers) as response:
                if response.content_type == 'application/json':
                    data = await response.json()
                    if response.status == 200 and "phone" in data:
                        return {
                            "id": data.get("id"),
                            "phone": data.get("phone"),
                            "price": data.get("price")
                        }
                    else:
                        logging.error(f"Ошибка при покупке номера (buy_number()): {response.status}, {data}")
                        return {"error": f"Ошибка {response.status}", "message": data.get("message", "Неизвестная ошибка")}
                else:
                    text = await response.text()
                    if "no free phones" in text.lower():
                        return {"error": "no_free_phones", "message": "К сожалению, номеров для данной страны нет. Попробуйте выбрать другую страну."}
                    raise Exception(f"Unexpected response: {text}")

    @staticmethod
    async def refund(order_id: int, max_retries: int = 5, delay: int = 60):
        headers = {
            "Authorization": f"Bearer {SIM5_API_KEY}",
            "Accept": "application/json"
        }

        for attempt in range(max_retries):
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{BASE_URL}/user/cancel/{order_id}", headers=headers) as response:
                    text = await response.text()
                    if response.status == 200:
                        return True
                    elif "you need to wait time" in text.lower():
                        logging.warning(f"Необходимо подождать перед возвратом средств. Попытка {attempt + 1} из {max_retries}. Ожидание {delay} секунд.")
                        await asyncio.sleep(delay)
                    else:
                        logging.error(f"Ошибка при возврате средств: {response.status}, Ответ: {text}")
                        return False

        logging.error(f"Не удалось выполнить возврат средств после {max_retries} попыток.")
        return False


    @staticmethod
    async def get_sms(order_id: str):
        headers = {
            "Authorization": f"Bearer {SIM5_API_KEY}",
            "Accept": "application/json"
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(f"{BASE_URL}/user/check/{order_id}", headers=headers) as response:
                logging.info(f"Статус ответа от 5sim: {response.status}")
                if response.status == 200:
                    data = await response.json()
                    logging.info(f"Ответ от 5sim: {data}")
                    sms = data.get("sms", [])
                    if sms:
                        return sms[0].get("code")
                    else:
                        logging.error("СМС-код не найден.")
                logging.error(f"Ошибка при получении кода: {response.status}")
                return None

