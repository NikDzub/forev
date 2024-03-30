#!/usr/bin/env python3


import asyncio
from playwright.async_api import async_playwright


async def scrape_products():

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

        #  --------------------------- get categories ---------------------------
        categories = []
        categories_selector_all = await page.query_selector_all(
            'a[href*="https://flpil.co.il/product-category/"]'
        )
        for category in categories_selector_all:
            href = await category.get_attribute("href")
            if "%" not in href and href not in categories:
                categories.append(href)
                print(href)

        #  --------------------------- get products from category ---------------------------
        products = []
        for category in categories:
            await page.goto(category, wait_until="load")
            print("-" * 10)
            print(category)
            products_selector_all = await page.query_selector_all(
                f'a[href*="https://flpil.co.il/shop/"]'
            )
            for product in products_selector_all:
                href = await product.get_attribute("href")
                if (
                    "3-pak" not in href
                    and href not in products
                    and href != "https://flpil.co.il/shop/"
                ):
                    products.append(href)
                    print(href)

        with open("./products.txt", "w") as outfile:
            for index, row in enumerate(products):
                outfile.write(str(row) + "\n")

        #  --------------------------- get product info ---------------------------
        for product in products:
            await page.goto(product, wait_until="load")
            product_images_selector_all = await page.query_selector_all(
                'img[role="presentation"]'
            )
            for img in product_images_selector_all:
                src = await img.get_attribute("src")
                print(src)

        print("here")
        await page.wait_for_timeout(546546456)

        await context.close()


async def main():
    await scrape_products()


asyncio.run(main())
