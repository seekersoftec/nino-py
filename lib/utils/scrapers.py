import logging
import os
import re
import scrapy
import random
import pandas as pd
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from googlesearch import search
#
from modules.useragents import *

logging.getLogger('scrapy').propagate = False

# The user agent we report to pages, and to google
USER_AGENT = random.choice(USER_AGENTS)
#
#
#


class GoogleSpider(scrapy.Spider):

    name = 'EmailScraper'

    def parse(self, response):

        links = LxmlLinkExtractor(allow=()).extract_links(response)
        links = [str(link.url) for link in links]
        links.append(str(response.url))

        for link in links:
            yield scrapy.Request(url=link, callback=self.parse_link)

    def parse_link(self, response):

        for word in self.reject:
            if word in str(response.url):
                return

        # html_text = str(response.text)
        # mail_list = re.findall('\w+@\w+\.{1}\w+', html_text)

        # dic = {'email': mail_list, 'link': str(response.url)}

        df = pd.DataFrame({'email': re.findall(
            '\w+@\w+\.{1}\w+', str(response.text))})

        df.to_csv(self.path, mode='a', header=False)
        df.to_csv(self.path, mode='a', header=False)


def get_urls(tag, n, language):
    urls = [url for url in search(tag, num_results=n, lang=language)][:n]
    return urls


def ask_user(question):
    response = input(question + ' y/n' + '\n')
    if response == 'y':
        return True
    else:
        return False


def create_file(path):
    response = False
    if os.path.exists(path):
        response = ask_user('File already exists, replace?')
        if response == False:
            return

    with open(path, 'wb') as file:
        file.close()


def get_info(tag, n, language, path, reject=[]):

    create_file(path)
    # df = pd.DataFrame(columns=['email', 'link'], index=[0])
    df = pd.DataFrame(columns=['email'], index=[0])
    df.to_csv(path, mode='w', header=True)

    print('Collecting Google urls...')
    google_urls = get_urls(tag, n, language)

    print('Searching for emails...')
    # process = CrawlerProcess({'USER_AGENT': USER_AGENT, 'Referer': 'http://www.google.com'})
    process = CrawlerProcess({'USER_AGENT': USER_AGENT})
    process.crawl(MailSpider, start_urls=google_urls, path=path, reject=reject)
    process.start()

    print('Cleaning emails...')
    df = pd.read_csv(path, index_col=0)
    # df.columns = ['email', 'link']
    df.columns = ['email']
    df = df.drop_duplicates(subset='email')
    df = df.reset_index(drop=True)
    df.to_csv(path, mode='w', header=True)

    return df


# class FacebookSpider(object):
#     def __init__(self, *args):
#         super(FacebookSpider, self).__init__(*args))
