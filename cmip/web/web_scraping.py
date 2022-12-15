import asyncio
from playwright.async_api import async_playwright
import os
import aiofiles
from io import BytesIO
from PIL import Image
import tqdm
from cmip.web.utils import url2domain, decode_image


async def event_handler_save_images(response, save_path) -> None:
    try:
        if not response.headers.get("content-type", "").startswith("image"):
            return
        if response.headers.get("content-type", "").startswith("image/svg"):
            return
        image = await response.body()
        if len(image) < 200:
            return
        file_hash = hash(os.path.basename(response.request.url))
        check_path = os.path.join(save_path, f"{file_hash}.jpg")
        if response.request.url.endswith("webp"):
            byte_stream = BytesIO(image)
            im = Image.open(byte_stream)
            im = im.convert("RGB")
            im.save(check_path)
        else:
            async with aiofiles.open(check_path, 'wb') as f:
                await f.write(image)
    except Exception as e:
        print(e)


async def get_web(url, save_path, save_images=True):
    try:
        async with async_playwright() as p:
            browser_type = p.chromium
            browser = await browser_type.launch()
            page = await browser.new_page()
            domain = url2domain(url)
            save_dir = os.path.join(save_path, domain)
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            if save_images:
                page.on("response", lambda response: asyncio.create_task(
                    event_handler_save_images(response, save_dir)))
            await page.goto(url, timeout=0)
            await page.wait_for_timeout(10000)
            # await page.wait_for_load_state("load")
            await page.reload(wait_until="networkidle")
            html = await page.content()
            async with aiofiles.open(os.path.join(save_path, domain, "dynamic.html"), 'w', encoding='utf-8') as f:
                await f.write(html)
            images = await page.query_selector_all('img')
            for idx, src in enumerate(
                    set([await page.evaluate('(element) => element.src', image) for image in images])):
                if src.startswith("data:image"):
                    async with aiofiles.open(os.path.join(save_path, domain, f"{idx}.jpg"), 'wb') as f:
                        await f.write(decode_image(src))
            # await page.screenshot(path=f'example-{browser_type.name}.png', full_page=True)
            await page.wait_for_load_state("domcontentloaded")
            await page.wait_for_load_state("networkidle")
            await browser.close()
    except Exception as e:
        # await browser.close()
        print(">>", e)
        return


def web_scraping(urls, save_path, batch_size=4, save_images=True):

    for _ in tqdm.tqdm(range(len(urls) // batch_size + 1), total=len(urls) // batch_size + 1, desc="Crawler Batchs:"):
        batch = urls[:batch_size]
        async def m(batch):
            await asyncio.gather(*[get_web(url, save_path, save_images) for url in batch])
        asyncio.run(m(batch))
        urls = urls[batch_size:]


if __name__ == '__main__':

    urls = ["https://baidu.com", "https://qq.com"]

    outdir = r"C:\data\家庭高危域名20221212"
    urls = []
    with open(r"C:\data\家庭下高危域名1212.txt", 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if os.path.exists(os.path.join(outdir, line, "dynamic.html")):
                # continue
                pass
            if not line.startswith("http"):
                line = "http://" + line
                urls.append(line)
    print("域名数量：", len(urls))

    for i in range(3):
        if i == 0:
            _urls = urls[70:]
        else:
            _urls = urls
        web_scraping(_urls, outdir, batch_size=10, save_images=(i % 2 == 0))



