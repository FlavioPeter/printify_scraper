#!/bin/bash

if command -v deactivate &> /dev/null
then
    # Deactivate the virtual environment
    deactivate
else
    echo "Virtual environment is not active."
fi

rm -rf venv-scraper/
python3 -m venv venv-scraper
source venv-scraper/bin/activate
pip3 install scrapy scrapy-rotating-proxies PyExecJS termcolor

: <<'EOF'
pip3 install jupyter ipykernel ipython
python3 -m ipykernel install --user --name=venv-scraper
touch test.ipynb
EOF