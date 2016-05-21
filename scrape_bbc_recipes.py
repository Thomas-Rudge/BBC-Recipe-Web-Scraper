#! python3
## WARNING ## WARNING ## WARNING ## WARNING ## WARNING ##
## This script will create a directory with over 11,000##
## html pages in the directory it is executed from!    ##
# -------------------------------------------------------------------------------
# Name:        BBC Food Recipes & Techniques
# Purpose:     Grab all the recipes from the BBC food website and
#              strip them down to basic html pages.
# Author:      Thomas Edward Rudge
#
# Created:     2016-5-17
# Copyright:   (c) Thomas Edward Rudge 2016
# Licence:     MIT
# -------------------------------------------------------------------------------


import bs4, os, requests, time


def remove_temp_data():
    '''
    Remove temporary files used during the process
    '''
    if os.path.isfile('bbc_sitemap.txt'):
        os.remove('bbc_sitemap.txt')

    if os.path.isfile('temp_data.txt'):
        os.remove('temp_data.txt')


def add_data_to_indexhtml():
    '''
    Add the search data to the search.html search_data div.
    '''
    ## Check the necessary files are present.
    if not os.path.isfile('search.html'):
        raise Exception("Couldn't find the search.html file!")
    elif not os.path.isfile('temp_data.txt'):
        raise Exception("Couldn't find the temp_data.txt file!")

    ## Get the search.html where the data will be inserted
    with open('search.html', 'r', encoding='utf-8') as f:
        html_data = f.read()

    ## Get the index where the data should be inserted
    insertion_index = html_data.find('<div id=search_data>')

    ## Add the search data to the html file
    ## The read data is sliced because the last character will be a delimiter
    with open('temp_data.txt', 'r') as data_file:
        with open('search.html', 'w', encoding='utf-8') as html_file:
            html_file.write(html_data[:insertion_index + 20] +
                            data_file.read()[:-1] +
                            html_data[insertion_index + 20:])


def get_sitemap():
    '''
    Get the BBC Food sitemap and save it to a local file.
    '''
    ## If the sitemap already exists, don't bother getting it again
    if os.path.isfile('bbc_sitemap.txt'):
        return

    page = None

    for attempt in range(1, 4):
        page = requests.get('http://www.bbc.co.uk/food/sitemap.xml')
        try:
            page.raise_for_status()
            break
        except requests.RequestException:
            time.sleep(attempt * 10)

    if not page:
        raise Exception('Failed to get sitemap.xml')

    sitemap = bs4.BeautifulSoup(page.text, 'xml')

    ## Write the recipe urls to a text file
    with open('bbc_sitemap.txt', 'w') as f:
        for line in sitemap.find_all('loc'):
            for string in line.stripped_strings:
                if string.startswith('http://www.bbc.co.uk/food/recipes/'):
                    f.write(string + '\n')


def make_repodir():
    '''
    Make the repositories where the html and css files will be stored
    '''
    cwd = os.getcwd()

    bbc_food_repo = os.path.join(cwd, 'BBC_Food_Repo')
    css_path = os.path.join(bbc_food_repo, 'css')

    try:
        if not os.path.isdir(bbc_food_repo):
            os.mkdir(bbc_food_repo)
        if not os.path.isdir(css_path):
            os.mkdir(css_path)
    except Exception as e:
        raise Exception(str(e))


def get_stylesheets():
    '''
    Get the stylesheets needed to display the pages properly.
    '''
    ## Get the first URL from the sitemap (assume all the pages share styles)
    with open('bbc_sitemap.txt', 'r') as f:
        url = f.readline()
    url = url.strip('\n')

    if not url:
        raise Exception('No urls found in sitemap!')

    page = None

    for attempt in range(1, 4):
        page = requests.get(url)
        try:
            page.raise_for_status()
            break
        except requests.RequestException:
            time.sleep(attempt * 10)

    if not page:
        raise Exception("Couldn't retrieve page: " + url)

    soup = bs4.BeautifulSoup(page.text, 'lxml')
    sheets = []

    ## Get the sheets' urls
    for link in soup.find_all('link'):
        if 'stylesheet' in link.get('rel'):
            sheets.append(link.get('href'))

    ## Now get and save the sheets
    for link in sheets:
        link = 'http:' + link if link.startswith('//') else link
        sheet = requests.get(link)
        try:
            sheet.raise_for_status()
        except requests.RequestException:
            continue

        filepath = os.path.join('BBC_Food_Repo', 'css', link.split('/')[-1])

        with open(filepath, 'w') as css:
            css.write(sheet.text)

    return sheets


def save_pages(css_links):
    '''
    Grab every web page in the BBC Food sitemap and
    save it as a local html file.
    '''
    ## Build the new header data
    for i, link in enumerate(css_links):
        css_links[i] = os.path.join('css', link.split('/')[-1])

    ## Create a file that will hold each page and key information
    with open('temp_data.txt', 'w') as f:
        f.write('')

    ## Cycle through the sitemap grabbing each recipe
    with open('bbc_sitemap.txt', 'r') as f:
        for line in f.readlines():
            line = line.strip('\n')
            page = requests.get(line)

            try:
                page.raise_for_status()
            except requests.RequestException:
                continue

            soup = bs4.BeautifulSoup(page.text, 'lxml')

            ## Update the data file
            data = [soup.find('h1', class_='content-title__text'),
                    '',
                    soup.find('div', class_='recipe-ingredients')
                    ]

            for i, datum in enumerate(data):
                if data[i]:
                    data[i] = datum.text.replace('\n', '')
                else:
                    data[i] = ''

            with open('temp_data.txt', 'a', encoding='utf-8') as tempfile:
                tempfile.write(line.split('/')[-1] + '~:]' + str(data)[1:-1].upper() + '~:]')

            ## Update the head tag
            soup.head.clear()
            for link in css_links:
                new_link = soup.new_tag('link')
                new_link.attrs['rel'] = 'stylesheet'
                new_link.attrs['href'] = link
                soup.head.append(new_link)

            ## Remove unwanted elements
            soup.header.decompose()
            decomp = [soup.find('div', class_='main-menu'),
                      soup.find('div', class_='food-wrapper'),
                      soup.find('div', class_='recipe-finder-link__wrap'),
                      soup.find('div', class_='grid-list-wrapper'),
                      soup.find('div', class_='recipe-actions'),
                      soup.find('div', class_='recipe-quick-links'),
                      soup.find('div', class_='recipe-extra-information__wrapper'),
                      soup.find('div', id='recipe-finder__box'),
                      soup.find('div', id='orb-footer'),
                      soup.find('div', id='blq-global'),
                      soup.find('a', class_='chef__image-link')]

            for noscript in soup.find_all('noscript'):
                decomp.append(noscript)
            for div in soup.find_all('div', class_='recipe-media'):
                decomp.append(div)
            for div in soup.find_all('div', class_='bbccom_display_none'):
                decomp.append(div)
            for script in soup.find_all('script'):
                decomp.append(script)

            for ele in decomp:
                if ele:
                    ele.decompose()

            ## Convert anchor tags into spans (links into text)
            tags = []
            for tag in soup.find_all('a'):
                tags.append(tag)
            for tag in tags:
                new_tag = soup.new_tag('span')
                new_tag.string = tag.text
                tag.replace_with(new_tag)

            ## Convert the soup back into html and save it to file
            html = soup.prettify()

            filepath = os.path.join('BBC_Food_Repo', line.split('/')[-1] + '.html')
            with open(filepath, 'w', encoding='utf-8-sig') as html_page:
                html_page.write(html)


def main():
    get_sitemap()

    make_repodir()

    stylesheets = get_stylesheets()

    save_pages(stylesheets)

    add_data_to_indexhtml()

    remove_temp_data()


if __name__ == '__main__':
    main()
