import scrapy
from scrapy_playwright.page import PageMethod
from termcolor import colored
from urllib.parse import urlencode
import json
import requests
import os

base_url = "https://printify.com"
# url = "https://printify.com/app/products/mens-clothing/long-sleeves"
base_prod_url = "https://printify.com/app/products/"
image_base_url = "https://printify.com/cdn-cgi/image/width=520,quality=100,format=avif/https://images.printify.com/api/catalog/"

cat_dict = {
    "mens-clothing": "Men's Clothing",
    "womens-clothing": "Women's Clothing",
    "kids-clothing": "Kids' Clothing",
    "food-health-beauty": "Food Health Beauty",
    "accessories": "Accessories",
    "home-and-living": "Home & Living",
}

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-CA,en-US;q=0.7,en;q=0.3",
    # 'Accept-Encoding': 'gzip, deflate, br, zstd',
    "X-Pfy-Currency": "USD",
    "X-AB-Test-Token": "fab09d1b-30c8-49f9-a548-7693708190fa",
    "Alt-Used": "printify.com",
    "Connection": "keep-alive",
    "Referer": "https://printify.com",
    # 'Cookie': 'lastRskxRun=1722448734090; rskxRunCookie=0; rCookie=4utxcs3l0u7pmnxub9uv4lz77va8g; fs_uid=#o-1N5X16-na1#6393ef88-46b0-4342-a2da-51160f9c5e1d:980031be-aa9a-4cc6-a9b5-098405a838a2:1722448704147::3#/1753807413; ajs_anonymous_id=50854190-770e-44ac-a1a2-6005aedf7393; _gcl_au=1.1.642978202.1722271312; _ga_4LD34WSM2H=GS1.1.1722448711.11.0.1722448711.60.0.0; _ga=GA1.1.1198590321.1722271312; _pin_unauth=dWlkPU4yVXlNbU13TXpZdE1XRmlOQzAwTlRWbUxXSTVOVFl0TnpRMVl6bG1NVGd4WVRFdw; _hp2_id.2463375893=%7B%22userId%22%3A%227986735525388334%22%2C%22pageviewId%22%3A%228595823310579458%22%2C%22sessionId%22%3A%224972604758979432%22%2C%22identity%22%3Anull%2C%22trackerVersion%22%3A%224.0%22%7D; _tt_enable_cookie=1; _ttp=d3OAdKJLmALKmw4b8BETw9aP1Uq; _fbp=fb.1.1722271313886.835156630507193436; _hp2_props.2463375893=%7B%7D; __cf_bm=aynyIv23DsrrfNrHmwKyq.1B_7FCySCN6ArbfQ9RS0g-1722448701-1.0.1.1-Nno4TDbG202BgHD1H4IKi.Z7NqFVEvLOEFPaSWymfHmvtoCKuk3NhtJPVAx35g_dcyWo19PRDUkeJ5yNE2c6tg; fs_lua=1.1722448734618; _hp2_ses_props.2463375893=%7B%22ts%22%3A1722448711711%2C%22d%22%3A%22printify.com%22%2C%22h%22%3A%22%2Fapp%2Fproducts%2Fmens-clothing%2Flong-sleeves%22%7D; _uetsid=760986304dc911ef9b34c98617dd2fc6; _uetvid=7609a1404dc911ef837737d97bcf3b61',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    # Requests doesn't support trailers
    # 'TE': 'trailers',
}

FOLDER_PATH = os.path.join(".", "data_scraped_test")
data_list = []


class PrintifySpider(scrapy.Spider):
    name = "printify"
    allowed_domains = ["printify.com"]

    def start_requests(self):
        cat = self.url_input.split("/")[-2]
        sub = self.url_input.split("/")[-1]
        params = {
            "page": "1",
            "limit": "200",
            "tags[]": [
                cat_dict[cat],
                (
                    sub.replace("-", " ").title()
                    if sub != "t-shirts"
                    else sub.capitalize()
                ),
            ],
            "target_market": "All markets",
            "bpp_target_market_filter": "1",
            "sort[popularity]": "desc",
        }
        api_url = (
            "https://printify.com/product-catalog-service/api/v1/blueprints/search"
        )
        encoded_params = urlencode(params, doseq=True)

        yield scrapy.Request(
            f"{api_url}?{encoded_params}",
            headers=headers,
            callback=self.parse,
        )

    def parse(self, response):
        products_data = response.json()["data"]
        one_product_url = (
            "https://printify.com/product-catalog-service/api/v1/blueprints/"
        )

        if products_data == []:
            print(
                colored(
                    "!!!!!!!!!!!!!!!!!!!! REQUEST HAD AN EMPTY RETURN !!!!!!!!!!!!!!!!!!!!",
                    "red",
                )
            )

        for pd in products_data:
            id = pd["blueprintId"]
            brand = pd["brandName"].replace("+", "").lower().replace(" ", "-")
            name = (
                pd["name"]
                .lower()
                .replace(" ", "-")
                .replace("(", "")
                .replace(")", "")
                .replace("'", "")
            )
            rel_pd_url = f"{id}/{brand}/{name}"

            partial_data = {
                "id": id,
                "name": pd["name"],
                "product_url": base_prod_url + rel_pd_url,
                "images": [image_base_url + image["src"] for image in pd["images"]],
                "price": float(
                    str(pd["minPrice"])[:-2] + "." + str(pd["minPrice"])[-2:]
                ),
                "price_sub": float(
                    str(pd["minPriceSubscription"])[:-2]
                    + "."
                    + str(pd["minPriceSubscription"])[-2:]
                ),
            }

            yield scrapy.Request(
                f"{one_product_url}{id}",
                meta={"partial_data": partial_data},
                callback=self.parse_product_page,
            )

    def parse_product_page(self, response):
        partial_data = response.request.meta["partial_data"]
        one_product_data = response.json()

        data = {
            **partial_data,
            "brand": one_product_data["brandName"],
            "details": one_product_data["details"],
            "description": one_product_data["description"],
            "features": [
                {"feature": f["name"], "detail": f["description"]}
                for f in one_product_data["features"]
            ],
            "care_instructions": [
                care["option"] for care in one_product_data["careSets"]
            ],
            "size_guide": one_product_data["sizeGuide"],
        }

        print(colored(f"Saving product: {data}", "green"))

        yield data
