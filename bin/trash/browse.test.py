from playwright.async_api import async_playwright
from playwright_stealth import stealth_async
from fake_useragent import UserAgent
from asyncio import sleep, run


async def main(tiktok: str) -> None | bool | tuple[bool, str, str, str]:
    try:
        arr = ["test_order_id", "669228659"]  # Фіктивне повернення з Grizzly
        number = arr[1]
        odr = arr[0]

        print("main", number, odr)
        ua = UserAgent()
        print(ua)
        async with async_playwright() as p:
            browser = await p.chromium.launch(channel="chrome", headless=False)
            context = await browser.new_context(user_agent=ua.safari)
            page = await context.new_page()

            await context.clear_cookies()


            await page.goto("https://www.tiktok.com/login/phone/forget-password")
            await sleep(10)
            await page.click('div[role="select"]')
            await page.click(f":text('{tiktok}')")

            field = page.locator('input[name="mobile"]')
            if not field:
                raise Exception("Could not find mobile input field")

            await field.click()
            await field.fill(str(number))
            await page.click(":text('Send code')")

            # Фіктивний код активації
            num = "123456"  # Заміна на фіктивний код
            if not num:
                return False

            code = page.locator('input[type="text"][placeholder="Enter 6-digit code"]')
            if not code:
                raise Exception("Could not find code input field")

            await code.click()
            await code.fill(num)

            password = "iiporol"# Генеруємо пароль
            pass_field = page.locator('input[type="password"][placeholder="Password"]')
            if not pass_field:
                raise Exception("Could not find password field")

            await pass_field.click()
            await pass_field.fill(password)
            await page.click(":text('Log in')")

            await browser.close()  # Закриваємо браузер після завершення

        return True, number, odr, password

    except Exception as e:
        print(f"Error in main: {e}")
        if odr:
            return None

run(main("+380"))
