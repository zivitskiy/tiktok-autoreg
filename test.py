from playwright.async_api import async_playwright
from asyncio import sleep, run

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel="chrome", headless=False)
        context = await browser.new_context(user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 7_0_8; en-US) AppleWebKit/533.38 (KHTML, like Gecko) Chrome/51.0.3140.246 Safari/600")
        page = await context.new_page()

        # await stealth_async(page)

        await page.goto("https://www.tiktok.com/login/phone/forget-password")
        await sleep(10000)

run(main())
