# BBC Recipe Web Scraper

The BBC are planning on removing over 11,000 recipes from their website. This scraper will create a local repository of those recipes on your computer.

The repo comes with a `search.html` page from which searches can be performed on the recipes scraped with the script. You can type one or more words and have the search match any or all terms lists.

![Search screen](http://i.imgur.com/MAsbdHd.jpg)

![Recipe screen](http://i.imgur.com/OAPABob.jpg)

:exclamation:**Warning: This script will create a folder with over 11,000 HTML files in it.**:exclamation:

I ran this overnight on my laptop and it took about 5 ½ hours. Total size is 108 MB, size on disk 129 MB. The search screen works perfectly fine on my computer (i5 4GB RAM Chrome), and only lags for about a second when bringing back all +11,000 recipes.

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