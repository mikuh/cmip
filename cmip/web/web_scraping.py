import asyncio
from playwright.async_api import async_playwright
import os
import aiofiles
from io import BytesIO
from PIL import Image
from tqdm.asyncio import tqdm
from cmip.web.utils import url2domain, decode_image


async def event_handler_save_images(response, folder, min_img_size=200) -> None:
    try:
        content_type = response.headers.get("content-type", "")
        if content_type.startswith("image") and not content_type.startswith("image/svg"):
            image = await response.body()
            url = response.request.url
            if len(image) > min_img_size:
                file_hash: int = hash(os.path.basename(url))
                _path: str = os.path.join(folder, f"{file_hash}={len(image)}.jpg")
                if url.endswith("webp"):
                    byte_stream = BytesIO(image)
                    im = Image.open(byte_stream)
                    im = im.convert("RGB")
                    im.save(_path)
                else:
                    async with aiofiles.open(_path, 'wb') as f:
                        await f.write(image)
    except Exception as e:
        print(f"Error saving image: {response.request.url}, {e}")


async def fetch_url(semaphore, browser, url, folder, save_image=True, min_img_size=200):
    async with semaphore:
        context = await browser.new_context()
        page = await context.new_page()
        if save_image:
            page.on("response", lambda response: asyncio.create_task(
                event_handler_save_images(response, folder, min_img_size)))
        try:
            await page.goto(url, wait_until="networkidle")
            content = await page.content()

            async with aiofiles.open(os.path.join(folder, "dynamic.html"), "w", encoding="utf-8") as f:
                await f.write(content)

            images = await page.query_selector_all('img')
            for idx, src in enumerate(
                    set([await page.evaluate('(element) => element.src', image) for image in images])):
                if src.startswith("data:image"):
                    async with aiofiles.open(os.path.join(folder, f"{idx}.jpg"), 'wb') as f:
                        await f.write(decode_image(src))

        except Exception as e:
            print(f"Error fetching URL: {url}, {e}")

        finally:
            await page.close()
            await context.close()


async def web_scraping(urls, output_path="output", max_concurrent_tasks=10, save_image=True, min_img_size=200):
    semaphore = asyncio.Semaphore(max_concurrent_tasks)
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        tasks = []
        for i, url in enumerate(urls):
            folder = os.path.join(output_path, url2domain(url))
            os.makedirs(folder, exist_ok=True)
            tasks.append(fetch_url(semaphore, browser, url, folder, save_image, min_img_size))
        try:
            for result in tqdm(asyncio.as_completed(tasks), total=len(tasks), desc="Fetching URLs"):
                await result
        except Exception as e:
            print(f"Error in main: {e}")
        finally:
            await semaphore.acquire()
            await browser.close()


if __name__ == "__main__":
    urls = [
        "https://baidu.com",
        "https://qq.com",
        # ...更多的URL
    ]
    asyncio.run(web_scraping(urls))
