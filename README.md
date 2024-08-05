# setup linux
python3 -m venv venv-scraper
source venv-scraper/bin/activate
pip3 install scrapy scrapy-rotating-proxies PyExecJS termcolor


# setup windows
python -m venv venv-scraper
.\venv-scraper\Scripts\activate
pip install scrapy scrapy-rotating-proxies PyExecJS termcolor

# to run
either run it sequentially (main_sequentially.py) or in parallel (main_parallel.py)