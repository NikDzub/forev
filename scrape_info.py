#!/usr/bin/env python3

import asyncio
from playwright.async_api import async_playwright
import requests
import os

products = []
with open("./products.txt") as f:
    for line in f.readlines():
        products.append(line.replace("\n", ""))


def download_image(url, output_path):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(output_path, "wb") as f:
                f.write(response.content)
            print(f"Image downloaded to {output_path}")
        else:
            print(
                f"Failed to download image from {url}. Status code: {response.status_code}"
            )
    except Exception as e:
        print(f"Error downloading image from {url}: {str(e)}")


async def scrape_info():

    async with async_playwright() as p:
        context = await p.firefox.launch(
            headless=False,
            # proxy={
            #     "server": "181.177.87.173:9291",
            #     "username": "3jFvwU",
            #     "password": "qF5DWZ",
            # },
        )
        page = await context.new_page(
            # user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"
        )
        await page.goto("https://flpil.co.il/", wait_until="load")

        #  --------------------------- get images ---------------------------
        for index, product in enumerate(products):
            print("-" * 30)
            images = []
            await page.goto(product, wait_until="load")

            try:
                info_selector = await page.query_selector(
                    'div[class*="prod_paragraph"]'
                )
                info = await info_selector.inner_text()

                icons_info_selector = await page.query_selector('[data-id="0c50763"]')
                await icons_info_selector.evaluate(
                    """e=>{e.style.backgroundColor = "orange";
                       e.style.padding = "15px"};"""
                )
                await page.wait_for_timeout(1000)

                title_selector = await page.query_selector(
                    'h1[class="product_title entry-title"]'
                )
                short_name = await title_selector.inner_text()
                try:
                    os.mkdir(f"./products/{index}")
                except:
                    pass

                png_selector_all = await page.query_selector_all('img[src*="png"]')
                jpg_selector_all = await page.query_selector_all('img[src*="jpg"]')

                for png in png_selector_all:
                    src = await png.get_attribute("src")
                    if (
                        src not in images
                        and "logo-forever" not in src
                        and "x100" not in src
                        and "share" not in src
                        and "Icon" not in src
                        and "vegan" not in src
                        and "animal" not in src
                        and "family" not in src
                    ):

                        images.append(src)
                for jpg in jpg_selector_all:
                    src = await jpg.get_attribute("src")
                    if (
                        src not in images
                        and "logo-forever" not in src
                        and "x100" not in src
                        and "share" not in src
                        and "Icon" not in src
                        and "vegan" not in src
                        and "animal" not in src
                        and "family" not in src
                    ):
                        images.append(src)

                for img_index, img in enumerate(images):
                    filename = f"image_{img_index}.jpg"
                    output_path = os.path.join(f"products/{index}", filename)
                    download_image(img, output_path)

                    with open(f"products/{index}/info.txt", "w") as outfile:
                        outfile.write(f"{short_name} - {info}")

                await icons_info_selector.screenshot(
                    path=f"products/{index}/icons_info.png"
                )

            except Exception as error:
                print(error)

        await context.close()


async def main():
    await scrape_info()


asyncio.run(main())
