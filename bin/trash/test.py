from playwright.async_api import async_playwright
from passwords import Generator
from config import *
from grizzly import Grizzly
from asyncio import run, sleep

passw = Generator()

async def Main(tiktok: str, ccode: str):
    # Задать фиксированные значения для теста
    number = "1234567890"  # Замените на тестовый номер
    odr = "test_order_id"   # Замените на тестовый идентификатор заказа
    test_code = "123456"     # Замените на тестовый код

    # Убрать вызов Grizzly.buy для теста
    # arr = await Grizzly.buy(code=ccode, event=event)

    # Имитация значений из arr
    # if arr is not None:
    #     number = arr[0]
    #     odr = arr[1]

    if number:
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(channel="chrome", headless=False)
                page = await browser.new_page()

                await page.goto("https://www.tiktok.com/login/phone/forget-password")
                await page.click('div[role="button"][aria-haspopup="true"]')
                await page.click(f":text('{tiktok}')")

                field = page.locator('input[name="mobile"]')

                if field:
                    await field.click()
                    await field.fill(number)  # Заполнить фиксированным номером

                # Удалено нажатие на кнопку "Send code"

                # Используем фиксированный код вместо получения кода через SMS
                num = test_code  # Используем тестовый код
                code = page.locator('input[type="text"][placeholder="Enter 6-digit code"]')

                if code:
                    print("found")
                    await code.click()
                    print("clicked")
                    await code.fill(num)
                    print("Filled")

                password = page.locator('input[type="password"][placeholder="Password"]')
                if password:
                    await password.click()
                    await password.fill(passw.get())
                await page.click(":text('Log in')")
                return True, number, odr
        except Exception as e:
            print(e)
            return False, number, odr

if __name__ == "__main__":
    run(Main("Kampuchea", "24"))
