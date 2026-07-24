"""Open a visible Edge window and save a user-authorized Xianyu login state locally."""

from __future__ import annotations

import argparse
import asyncio
import time
from pathlib import Path

from playwright.async_api import async_playwright


ACCOUNT_COOKIE_NAMES = {
    "cookie2",
    "sgcookie",
    "unb",
    "lgc",
    "tracknick",
}


def has_account_cookie(cookies: list[dict]) -> bool:
    """Return True only when a known Alibaba account cookie is present."""
    names = {str(cookie.get("name", "")).lower() for cookie in cookies}
    return bool(names & ACCOUNT_COOKIE_NAMES)


def is_login_url(url: str) -> bool:
    lowered = (url or "").lower()
    return "passport.goofish.com" in lowered or "mini_login" in lowered


async def capture(output: Path, timeout_minutes: int) -> int:
    output.parent.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(
            channel="msedge",
            headless=False,
            args=["--disable-blink-features=AutomationControlled"],
        )
        context = await browser.new_context(no_viewport=True)
        page = await context.new_page()
        await page.goto("https://www.goofish.com/", wait_until="domcontentloaded")

        print("请在打开的 Edge 窗口中使用闲鱼扫码或本人手机号登录。")
        print("登录状态只会保存到本机，不会打印 Cookie 内容。")
        deadline = time.monotonic() + timeout_minutes * 60
        detected_at = None

        while time.monotonic() < deadline:
            cookies = await context.cookies()
            active_urls = [open_page.url for open_page in context.pages]
            account_ready = has_account_cookie(cookies)
            away_from_login = any(url and not is_login_url(url) for url in active_urls)
            if account_ready and away_from_login:
                detected_at = detected_at or time.monotonic()
                if time.monotonic() - detected_at >= 3:
                    await context.storage_state(path=str(output))
                    print(f"登录成功，状态已保存到：{output}")
                    await browser.close()
                    return 0
            else:
                detected_at = None
            await asyncio.sleep(2)

        print(f"在 {timeout_minutes} 分钟内未检测到登录，未保存状态。")
        await browser.close()
        return 1


def main() -> int:
    parser = argparse.ArgumentParser(description="安全采集闲鱼登录状态")
    parser.add_argument("--output", default="state/acc_1.json")
    parser.add_argument("--timeout-minutes", type=int, default=10)
    args = parser.parse_args()
    if args.timeout_minutes < 1 or args.timeout_minutes > 30:
        parser.error("--timeout-minutes 必须在 1 到 30 之间")
    return asyncio.run(capture(Path(args.output).resolve(), args.timeout_minutes))


if __name__ == "__main__":
    raise SystemExit(main())
