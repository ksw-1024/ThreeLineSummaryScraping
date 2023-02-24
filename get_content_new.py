import requests
from bs4 import BeautifulSoup
from bs4.element import NavigableString
import re
import html5lib
import time
import csv

# defined
summary = []
summary_number = 0
page_start = 1
page_end = 10

print("Start scraping Livedoor News.")

while page_start < page_end:
    url = 'https://news.livedoor.com/topics/category/main/?p=' + str(page_start)
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/110.0"
    }
    res = requests.get(url, headers=headers)

    soup = BeautifulSoup(res.text, "html5lib")

    links_list = soup.find(class_="articleList")
    links = links_list.find_all(href=re.compile("https://news.livedoor.com/topics/detail"))
    # links = soup.find_all()

    pickup_links = [link.attrs['href'] for link in links]

    for pickup_link in pickup_links:
        time.sleep(5)
        pickup_res = requests.get(pickup_link, headers=headers)
        pickup_soup = BeautifulSoup(pickup_res.text, "html5lib")
        print("GET: " + pickup_link)

        find_summary = pickup_soup.find(class_="summaryList")
        if find_summary is not None:

            get_article_link = pickup_soup.find(href=re.compile("https://news.livedoor.com/article/detail"))
            time.sleep(1)
            article_res = requests.get(get_article_link.attrs["href"], headers=headers)
            article_soup = BeautifulSoup(article_res.text, "html5lib")

            article = ""

            lineList = article_soup.select('.articleBody p')
            for line in lineList:
                if len(line.contents) > 0 and type(line.contents[0]) == NavigableString:
                    article += line.contents[0].strip()
            print("INDEX: " + article)

            li_list = []
            for li in find_summary.find_all("li"):
                li_list.append(li.text)
            summary.append(li_list)
            summary[summary_number].append(article)

            summary_number += 1
        else:
            print("No summary minutes were found on this page.")

    with open('output.csv', 'w') as file:
        writer = csv.writer(file, lineterminator='\n')
        writer.writerows(summary)
        print("Successful output.")

    page_start = page_start + 1
