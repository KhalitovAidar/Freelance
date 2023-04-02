import asyncio
from playwright.async_api import Playwright, async_playwright
import requests


async def solve_captcha(page: Playwright) -> bool:
    captcha_response = requests.post("https://api.capmonster.cloud/in.php", data={
        "clientKey": "c4afaddfe95cd9de77c6998103b44100",
        "method": "hcaptcha",
        "sitekey": "f8ccefec-3bf6-4b6f-a044-4638e6dc36cf",
        "pageurl": page.url,
    })
    captcha_id = captcha_response.text.split("|")[1]

    while True:
        await page.waitForLoadState("domcontentloaded")
        if "captcha" not in page.url:
            return True

        captcha_solution = requests.get(
            f"https://api.capmonster.cloud/res.php?key=YOUR_CAPMONSTER_API_KEY&action=get&id={captcha_id}"
        ).text
        if captcha_solution == "CAPCHA_NOT_READY":
            await asyncio.sleep(1)
            continue
        else:
            await page.fill("#challenge-form [name='h-captcha-response']", captcha_solution)
            await asyncio.sleep(1)
            await page.click("#challenge-form [type='submit']")


async def login_to_zoom(meeting_link: str, passcode: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.newPage()

        await page.goto(meeting_link)

        if "Invalid" in await page.title():
            print("ссылка битая")
            return

        if "Enter passcode to join the meeting" in await page.innerText(".passcode-screen__title"):
            await page.fill(".passcode-screen__input", passcode)
            await page.click(".passcode-screen__join-button")

        if "Wrong passcode." in await page.innerText(".passcode-screen__error-message"):
            print(f"пасскод {passcode} не верный!")
            return

        if "captcha" in page.url:
            print("решаю капчу")
            await solve_captcha(page)

        if "zoom.us/wc/" in page.url:
            print("Успешная авторизация")
            print(await page.title())

        await browser.close()

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(login_to_zoom("https://us02web.zoom.us/rec/component-page?action=viewdetailpage&sharelevel=meeting&useWhichPasswd=meeting&clusterId=us02&componentName=need-password&meetingId=V3soCavoicqOvbWfyOZ6Smpp5bCsrO-71fbU5WdLt2StVVqegJIbwIx3pjI1VhYV.c9Fr_lxqDeQ2Abg3&originRequestUrl=https%3A%2F%2Fus02web.zoom.us%2Frec%2Fshare%2FA8_UYE2dgm3_4fpGW_jtZkoh8mmLbftdK8b7nkCDzSY6kkt7kzwFTVgA_g9XwIo1.9u0Fjzj_YruX72zC", "=CV0=9hN"))
