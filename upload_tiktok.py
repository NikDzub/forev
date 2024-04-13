#!/usr/bin/env python3


import asyncio
from playwright.async_api import async_playwright
import os


all_folders = os.listdir("./products")


async def scrape_products():

    async with async_playwright() as p:
        context = await p.firefox.launch_persistent_context(
            user_data_dir="./firefox",
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

        # await page.wait_for_timeout(546546456)

        async def chose_video(path):

            await page.goto(
                "https://www.tiktok.com/",
                wait_until="load",
            )

            await page.wait_for_timeout(54654645)
            await page.goto(
                "https://www.tiktok.com/creator#/upload?scene=creator_center",
                wait_until="load",
            )

            # chose the video
            async with page.expect_file_chooser() as fc_info:
                upload_btn = await page.wait_for_selector(
                    'div[class*="upload-container"]'
                    # 'div[class*="file-select-button"]'
                )

                await upload_btn.click(force=True)
                file_chooser = await fc_info.value
            await file_chooser.set_files(f"products/{path}/product_video_0.mp4")

            # wait for upload
            await page.wait_for_selector('video[class*="candidate-vide"]')
            info = await page.wait_for_selector('span[data-text="true"]')

            # set info
            with open(f"products/{path}/info.txt", "r") as file:
                info_txt = file.read()
                await info.fill(info_txt)

            # wait for uplaod

            for i in range(10):
                await page.keyboard.press("Tab")
            await page.keyboard.press("Enter")

            # post = await page.wait_for_selector('div[class*="btn-post"] button')

            await page.wait_for_selector('div[class*="uploaded-modal"]')

            print(f"uploaded - /products/{path}")

        for folder in all_folders:
            folder_content = os.listdir(f"./products/{folder}")

            used = ["59", "56", "33", "20", "0", "28", "1", "19", "36", "62", "37"]

            if "product_video_0.mp4" in folder_content and folder not in used:
                print(folder)
                await chose_video(folder)

        await page.close()
        await context.close()


asyncio.run(scrape_products())
