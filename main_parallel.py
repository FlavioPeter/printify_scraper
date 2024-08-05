import os
from twisted.internet import asyncioreactor

asyncioreactor.install()  # Install the asyncio reactor at the very beginning

import os
import execjs
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from printify_scraper.spiders.printify import PrintifySpider
from termcolor import colored

from twisted.internet import reactor


# List of URLs to crawl
def get_urls_array(path="urls.js"):
    # Read the content of the JavaScript file
    with open(path, "r", encoding="utf-8") as file:
        js_code = file.read()

    # Initialize the JavaScript runtime environment
    context = execjs.compile(js_code)

    # Extract the array (ensure the variable name matches the one in your .js file)
    urls = context.eval("categoryUrls")

    return urls


url_list = get_urls_array()

# url_list = [
#     "https://printify.com/app/products/mens-clothing/long-sleeves",
#     "https://printify.com/app/products/mens-clothing/tank-tops",
#     "https://printify.com/app/products/mens-clothing/sportswear",
# ]

FOLDER_PATH = os.path.join(".", "data_scraped")


def remove_files_in_folder(folder_path=FOLDER_PATH):
    # List all files in the specified folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        try:
            # Check if the path is a file and then remove it
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.remove(file_path)
                print(f"Removed file: {file_path}")
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")


def generate_output_filepath(url):
    cat = url.split("/")[-2]
    sub = url.split("/")[-1]
    file_name = f"{cat}_{sub}.json"
    file_path = os.path.join(FOLDER_PATH, file_name)
    return file_path


if __name__ == "__main__":
    if not os.path.exists(FOLDER_PATH):
        os.makedirs(FOLDER_PATH)
    remove_files_in_folder()

    settings = get_project_settings()

    for url in url_list:
        output_filepath = generate_output_filepath(url)
        # Make sure to add the JSON Feed Exporter
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

        process = CrawlerProcess(settings)
        process.crawl(PrintifySpider, url_input=url)
    process.start(
        stop_after_crawl=True
    )  # the script will block here until the last crawl is finished
    # try:
    #     reactor.run()  # Start the Twisted reactor
    # except:
    #     print(colored("Finished", "red"))

    # process.start()  # the script will block here until the last crawl is finished
