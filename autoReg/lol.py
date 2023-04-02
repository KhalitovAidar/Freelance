import asyncio
from playwright.sync_api import Playwright, Browser, Page


async def run(url: str, passcode: str) -> None:
    async with Playwright() as p:
        browser: Browser = await p.chromium.launch(headless=True)
        page: Page = await browser.new_page()
        await page.goto(url)
        try:
            await page.fill('input[type="password"]', passcode)
            await page.click('button[type="submit"]')
            await page.wait_for_selector('.zm-modal-footer .zm-btn.zm-btn-primary', timeout=10000)
            print("Успешная авторизация")
        except Exception as e:
            if "incorrect" in str(e):
                print(f"Пасскод {passcode} неверный!")
            elif "captcha" in str(e):
                print("Решаю капчу")
                await page.solve_recaptchas()
                await page.click('button[type="submit"]')
                await page.wait_for_selector('.zm-modal-footer .zm-btn.zm-btn-primary', timeout=10000)
                print("Успешная авторизация")
            elif "join a meeting" in str(e):
                print("Ссылка битая")
            else:
                raise e
        finally:
            title = await page.title()
            print(f"Заголовок страницы: {title}")
            await browser.close()


if __name__ == '__main__':
    asyncio.run(run(url='https://us02web.zoom.us/rec/component-page?action=viewdetailpage&sharelevel=meeting&useWhichPasswd=meeting&clusterId=us02&componentName=need-password&meetingId=V3soCavoicqOvbWfyOZ6Smpp5bCsrO-71fbU5WdLt2StVVqegJIbwIx3pjI1VhYV.c9Fr_lxqDeQ2Abg3&originRequestUrl=https%3A%2F%2Fus02web.zoom.us%2Frec%2Fshare%2FA8_UYE2dgm3_4fpGW_jtZkoh8mmLbftdK8b7nkCDzSY6kkt7kzwFTVgA_g9XwIo1.9u0Fjzj_YruX72zC',
                    passcode='=CV0=9hN'))
