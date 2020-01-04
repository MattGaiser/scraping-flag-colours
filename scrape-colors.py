import mechanicalsoup
from bs4 import BeautifulSoup
import re
import json


def extract_title(page):
    return page.find("header").find("h1").contents[0]



def extract_colours(page):
    color_list = page.find("ul")
    return list(dict.fromkeys(re.findall("#\w+", str(color_list.contents))))


def get_colours_from_page(browser, baseurl, target_page):
    response = browser.open(baseurl + target_page)
    soup = BeautifulSoup(response.text, 'lxml')
    extract = soup.find("section", {"id": "item"})
    entity = {"title": extract_title(extract), "colours": extract_colours(extract)}
    return entity

def get_links_from_article(articles):
    links = []
    for article in articles:
        links.append(article.find("a").attrs['href'])
    return links


def scrape_flag_pagination_page(browser, baseurl, pageCount):
    response = browser.open(baseurl + "/flags?page={0}".format(pageCount))
    soup = BeautifulSoup(response.text, 'lxml')
    flag_articles = soup.findAll("article")
    return get_links_from_article(flag_articles)



baseurl = "https://encycolorpedia.com"
browser = mechanicalsoup.StatefulBrowser(raise_on_404=True)
list_of_urls = []
flag_count = 0
pageCount = 1
while(True):
    try:
        list_of_urls += scrape_flag_pagination_page(browser, baseurl, pageCount)
    except mechanicalsoup.utils.LinkNotFoundError:
        break
    pageCount += 1
package = []
for url in list_of_urls:
    package.append(get_colours_from_page(browser, baseurl, url))

with open('flag_colours.json', 'w', encoding='utf-8') as f:
    json.dump(package, f, ensure_ascii=False, indent=4)