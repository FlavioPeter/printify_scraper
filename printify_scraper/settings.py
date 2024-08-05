import os

BOT_NAME = "printify_scraper"

# SCRAPEOPS
SCRAPEOPS_API_KEY = "c783b496-52f6-4db1-a308-181e6ae49afa"
SCRAPEOPS_FAKE_USER_AGENT_ENDPOINT = "https://headers.scrapeops.io/v1/user-agents"
SCRAPEOPS_FAKE_USER_AGENT_ENABLED = True
SCRAPEOPS_NUM_RESULTS = 50

# ROTATING_PROXY_LIST = [
#     "178.128.232.123:8080",
#     "192.99.37.195:16166",
#     "132.148.167.243:15664",
#     "67.213.210.118:30547",
#     "104.129.199.81:10160",
#     "136.226.65.104:10160",
#     "45.196.148.8:5432",
# ]

SPIDER_MODULES = ["printify_scraper.spiders"]
NEWSPIDER_MODULE = "printify_scraper.spiders"

TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 5

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = False

# Enable or disable downloader middlewares
DOWNLOADER_MIDDLEWARES = {
    "printify_scraper.middlewares.ScrapeOpsFakeUserAgentMiddleware": 400,
    "printify_scraper.middlewares.PrintifyScraperDownloaderMiddleware": 543,
    # "rotating_proxies.middlewares.RotatingProxyMiddleware": 610,
    "rotating_proxies.middlewares.BanDetectionMiddleware": 620,
}

# Enable and configure the AutoThrottle extension (optional, but often useful)
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 15  # The initial download delay
AUTOTHROTTLE_MAX_DELAY = 60  # The maximum download delay in case of high latencies
AUTOTHROTTLE_TARGET_CONCURRENCY = (
    1.0  # Average number of requests Scrapy should be sending in parallel
)
AUTOTHROTTLE_DEBUG = False  # Disable throttling stats

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
FEED_EXPORT_ENCODING = "utf-8"
