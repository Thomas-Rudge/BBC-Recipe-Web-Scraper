# BBC Recipe Web Scraper

:exclamation:**Warning: This script will create a folder with over 11,000 HTML files in it.**:exclamation:

The BBC are planning on removing over 11,000 recipes from their website. This scraper will create a local repository of those recipes on your computer.

The repo comes with a `search.html` page from which searches can be performed on the recipes scraped with the script. You can type one or more words and have the search match any or all terms lists.

![Search screen](http://i.imgur.com/MAsbdHd.jpg)

![Recipe screen](http://i.imgur.com/OAPABob.jpg)

## Instructions

1. Install the dependencies:

```python
pip install beautifulsoup4
pip install requests
```

2. Download the script and run it:

```bash
git clone https://github.com/Thomas-Rudge/BBC-Recipe-Web-Scraper.git
cd BBC-Recipe-Web-Scraper
python scrape_bbc_recipes.py
```
I would recommend running it overnight as it will take a while.