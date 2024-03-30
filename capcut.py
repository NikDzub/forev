#!/usr/bin/env python3

import mod
import os

import asyncio
from playwright.async_api import async_playwright

# files = os.listdir("./products")
# for file in files:
#     if file != ".DS_Store":
#         print(file + "-----")

#         images = os.listdir(f"./products/{file}")
#         for img in images:
#             if img != ".DS_Store":
#                 print(img)


async def capcut():

    async with async_playwright() as p:
        context = await p.firefox.launch(
            headless=False,
        )
        mod.clean_firefox()
        context = await p.firefox.launch_persistent_context(
            user_data_dir="./firefox", headless=False
        )

        page = await context.new_page()
        await page.goto("https://www.capcut.com/editor", wait_until="load")

        await page.wait_for_timeout(454545434)

        products_folder = await page.wait_for_selector(
            'div[class*="card-item__content"]'
        )
        await products_folder.click()
        await page.wait_for_timeout(2000)

        await page.wait_for_selector('div[class*="card-item__content"]')
        product_folders = await page.query_selector_all(
            'div[class*="card-item__content"]'
        )

        for folder in product_folders:
            await folder.click()
            folder_name_selector = await page.query_selector(
                'div[class*="folder-name"]'
            )
            folder_name = await folder_name_selector.inner_text()

            print(folder_name)

            back_btn_selector = await page.wait_for_selector('div[class*="back-btn"]')

            await back_btn_selector.click()

            await page.wait_for_timeout(2000)

        print("here")
        await page.wait_for_timeout(454545434)


async def main():

    await capcut()


asyncio.run(main())
