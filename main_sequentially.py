import os

# Ensure the asyncio reactor is installed before all imports
import sys
from twisted.internet import selectreactor

if "twisted.internet.reactor" in sys.modules:
    del sys.modules["twisted.internet.reactor"]
from twisted.internet import asyncioreactor

asyncioreactor.install()
from twisted.internet import defer, reactor

import execjs
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from termcolor import colored
from printify_scraper.spiders.printify import PrintifySpider


def get_urls_array(path="urls.js"):
    with open(path, "r", encoding="utf-8") as file:
        js_code = file.read()

    context = execjs.compile(js_code)
    urls = context.eval("categoryUrls")
    return urls


url_list = get_urls_array()

FOLDER_PATH = os.path.join(".", "data_scraped")


def generate_output_filepath(url):
    cat = url.split("/")[-2]
    sub = url.split("/")[-1]
    file_name = f"{cat}_{sub}.json"
    file_path = os.path.join(FOLDER_PATH, file_name)
    return file_path


def crawl_urls_sequentially(process, urls):
    if not urls:
        reactor.stop()  # Stop the reactor when all URLs have been crawled
        return

    while True:
        url = urls.pop(0)  # Get the first URL from the list
        output_filepath = generate_output_filepath(url)
        if not os.path.isfile(output_filepath):
            break

    settings = process.settings

    # Update settings for each spider configuration
    settings.update(
        {
            "FEEDS": {
                output_filepath: {
                    "format": "json",
                },
            },
            "TELNETCONSOLE_ENABLED": False,  # Disable Telnet Console
        }
    )

    def on_spider_closed(spider):
        # When the spider closes, start the next crawl
        crawl_urls_sequentially(process, urls)

    process.crawl(PrintifySpider, url_input=url).addCallback(on_spider_closed)
    process.start(
        stop_after_crawl=False
    )  # Start the crawl process but don't stop the reactor


if __name__ == "__main__":
    if not os.path.exists(FOLDER_PATH):
        os.makedirs(FOLDER_PATH)

    settings = get_project_settings()
    process = CrawlerProcess(settings)

    crawl_urls_sequentially(process, url_list)

    try:
        reactor.run()  # Start the Twisted reactor
    except:
        print(colored("Finished", "red"))
