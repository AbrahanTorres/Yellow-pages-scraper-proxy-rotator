# YELLOW PAGES SCRAPER

## Script Summary

This python script is used to scrape data from a yellow pages website called "Paginas Amarillas" using the Selenium web automation framework and BeautifulSoup for data extraction. The data is then stored in a PostgreSQL database using the SQLAlchemy library.

The script begins by importing various Python libraries, including pathlib, datetime, sys, logging, platform, warnings, json, phonenumbers, pandas, urlib.parse, and Selenium.

The main() function is the defined, which sets up the database connection and loads a list of pages to be scraped. The script the launches a Firefox browser using the GeckoDriverManager, nabigates to the "Paginas Amarillas" website, and accepts the cookie disclaimer. After this, the script navigates to each page in the list and scrapes the relevant data using BeautifulSoup. The data is then stored in the PostgreSQL database using SQLAlchemy.

If an error occurs at any point during the script's execution, it is logget to a file for later analysis.

## Script Requirements
The script requires the following libraries to be installed:

- pathlib
- datetime
- sys
- logging
- platform
- warnings
- json
- phonenumbers
- pandas
- sqlalchemy
- urllib
- selenium
- BeautifulSoup

In addition, a PostgreSQL database must be set up and the appropiate connection details provided to the script in order to store the scraped data.

## Script Usage
To use the script, simply execute it using the Python interpreter:

```python
python script_yellow_pages.py
```

Note that the script expects the database connection details to be provided via enviroment variables, specifically:


- ddbb_user
- ddbb_pass
- ddbb_name

You can specify them in the directory called library in the file called: environment_variables.json

Alternatively these can be set using the export command on Unix-based systems:

```bash
export ddbb_user=yourusername
export ddbb_pass=yourpassword
export ddbb_name=yourdatabasename
```

On Windows, the equivalent command is:

```bash
set ddbb_user=yourusername
set ddbb_pass=yourpassword
set ddbb_name=yourdatabasename
```

# Python Proxy Rotator

It is important to let you know that there are also a Python proxy rotator script called proxy_rotator.py

This is a Python script that enables web scraping without getting blocked by changing the proxy server constantly. It retrieves free proxies from the website "https://free-proxy-list.net/" and rotates through them while sending requests to the desired URLs.

## Getting Started

To run this script, you need to have Python 3.x installed in your system. You can download it from the official website: https://www.python.org/downloads/

You also need to install the following Python libraries:

- requests
- lxml
- bs4
- pandas

You can install them by running the following command:
```bash
pip install requests lxml bs4 pandas
```

## Usage
To use this script, you need to set up the URLs you want to scrape by modifying the urls list variable at the beginning of the script.

You can also change the maximum number of retries and the time threshold for a proxy to be considered as working by modifying the max_attempts and tiempo variables, respectively.

To run the script, open a terminal or command prompt in the directory where the script is located and run the following command:

```bash
python proxy_rotator.py
```

The output of the script will be saved to a CSV file named mydf3.csv in the same directory.

## Contributing
This script is open to contributions. Feel free to fork the repository and submit a pull request with your changes.




