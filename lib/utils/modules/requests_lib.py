
#
import sys
import logging
import threading
import requests
#
from bs4 import BeautifulSoup
#
from requests_futures.sessions import FuturesSession
#
from torpy.http.requests import tor_requests_session
#
import asyncio
from dataclasses import dataclass, field
from pyppeteer import launch
#


class AsyncRequests:
    #
    """
        Asynchronous requests
        method(s): request, map
    """

    def __init__(self):
        self.session = FuturesSession(session=requests.session())

    #
    def request(self, **kwargs):
        return self.session.request(**kwargs)

    #
    def map(self, requests: list):
        responses = []
        for i in range(len(requests)):
            responses.append(requests[i].result())

        #
        return responses

#


class TorRequests:
    def __init__(self):
        super().__init__()

    def get(self, url):
        try:
            with tor_requests_session() as currentSession:  # returns requests.Session() object
                _res = currentSession.get(url)
        except:
            with tor_requests_session() as currentSession:  # returns requests.Session() object
                _res = currentSession.get(url)

        return _res


#
#
# https://www.scraperapi.com/blog/best-10-free-proxies-and-free-proxy-lists-for-web-scraping/
# https://stackoverflow.com/questions/57227194/building-a-proxy-rotator-with-specific-url-and-script
# https://github.com/doubledare704/spys_one_proxy
# PROXY
def process_text_list(l_text: list) -> list:
    if "Squid" in l_text[2] or "Mikrotik" in l_text[2]:
        l_text[1] = f"{l_text[1]} {l_text[2]}"
        del l_text[2]
    del l_text[-5:len(l_text)]
    if ")" in l_text[-1]:
        l_text.append("-")

    try:
        float(l_text[-4])
    except ValueError:
        pass
    else:
        l_text[-4] = float(l_text[-4])
        l_text[3] = " ".join(l_text[3:-4])
        del l_text[4:-4]

    if "%" in l_text[-3]:
        l_text[-3] = int(l_text[-3].strip("%")) / 100
    return l_text


@dataclass
class Spys:
    proxy_list: list = None
    countries: list = field(default_factory=list)
    any_country: bool = False
    europe: bool = False
    north_america: bool = False

    async def search(self):
        if self.any_country:
            self.countries.extend(['DE', 'US', 'FR', 'UA', 'RU', 'PL', 'NL'])
            await self.pyppeteer_get_proxy_list()
        elif not self.any_country and self.countries:
            await self.pyppeteer_get_proxy_list()
        elif self.europe:
            await self.pyppeteer_get_proxy_list(url="http://spys.one/europe-proxy/")
        elif self.north_america:
            await self.pyppeteer_get_proxy_list(url="http://spys.one/north-america-proxy/")

    async def pyppeteer_get_proxy_list(self, url=None):
        country_list = self.countries
        browser = await launch(options={'args': ['--no-sandbox']})
        page = await browser.newPage()
        proxy_table = []
        await page.setUserAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36")
        if self.europe or self.north_america:
            # if europe or america method will accept url option
            country_list = ['42']
        for country in country_list:
            page_url = url or f'http://spys.one/free-proxy-list/{country}/'
            await page.goto(page_url)
            await asyncio.gather(
                page.select('tbody #xpp', '5'),
                page.waitForSelector('tbody #xpp'),
                page.keyboard.press("Enter"),
                page.waitFor(1500)
            )
            table = await page.JJ("tr.spy1xx")
            logging.debug(f"Started working with table: {len(table[1:])} ips")
            for index, item in enumerate(table[1:]):
                str_text = await page.evaluate('(element) => element.innerText', item)
                list_text = str_text.split()
                list_text = process_text_list(list_text)
                proxy_table.append(list_text)
            logging.debug("Finished working with table")
            await asyncio.sleep(3)
        await browser.close()
        self.proxy_list = proxy_table

    # async def get_https_based_proxies(self):
    #     page_url = 'https://spys.one/en/https-ssl-proxy/'
    #     browser = await launch(options={'args': ['--no-sandbox']})
    #     page = await browser.newPage()
    #     proxy_table = []
    #     await page.setUserAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    #                             "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36")

    #     page.goto(page_url)

#
#


def format_proxy(proxy):
    if isinstance(proxy, dict):  # checking if proxy is already formatted
        return proxy
    # raw_ip_and_port = proxy[0] + ":" + proxy[1]
    http = "http://" + proxy[0] + ":" + proxy[1]
    https = "https://" + proxy[0] + ":" + proxy[1]
    proxy_dict = {
        # "raw": raw_ip_and_port,
        "http": http,
        "https": https
    }
    return proxy_dict
#


def test_proxy(proxy_, verbose=False):
    logger = logging.getLogger()
    url = "https://www.iplocation.net/find-ip-address"
    if verbose:
        logger.info("testing proxy...")
    try:
        page = requests.get(url, proxies=proxy_)
        soup = BeautifulSoup(page.content, "html.parser")
        ip_tbl = soup.find("table", {"class": "iptable"})
        data = ip_tbl.find_all("td")
        ip = data[0].find("span").text
        location = data[1].text.split("[")[0]
        device = data[4].text + ", " + data[3].text
        os = data[5].text
        browser = data[6].text
        user_agent = data[7].text
        if verbose:
            logger.info(
                "\n\nSuccess! Able to connect with proxy\nConnection Details:\nip: " + ip + "\nlocation: " + location)
            logger.info("device: " + device + "\nos: " + os +
                        "\nbrowser: " + browser + "\nuser agent: " + user_agent)
        return 1
    except requests.exceptions.ProxyError:
        if verbose:
            logger.error("request caused a proxy error!")
        return 0
    except AttributeError:
        if verbose:
            logger.error("Something went wrong.")
        return 0
#
#


def get_proxies_by_country(country='DE'):
    try:
        loop = asyncio.get_event_loop()
        spys = Spys()
        spys.countries.append(country)
        loop.run_until_complete(spys.search())
        # print(spys, spys.proxy_list)
        return spys.proxy_list
    except Exception as e:
        # print('An Error Occurred: '+str(e))
        return e


def filter_proxies(proxies: list, threshold: int = 0.7, proxy_type: str = 'http'):
    _results = []

    for proxy in proxies:
        # print(proxy[1])
        try:
            if ((float(proxy[5]) > threshold) and (proxy_type.lower() in str(proxy[1]).lower())):
                _results.append(proxy)
        except Exception as e:
            pass
    #
    return _results


#
#
#
if __name__ == '__main__':
    proxies = get_proxies_by_country()
    print(proxies)
    filtered_proxies = filter_proxies(proxies=proxies)
    print(filtered_proxies)
    #
    for i in range(len(proxies)):
        # print(proxies[i][0])
        addr = [proxies[i][0].split(':')[0], proxies[i][0].split(':')[1]]
        proxy = format_proxy(addr)
        res = test_proxy(proxy_=proxy)
        if (res == 1):
            print(f'success! => {proxy}')
        else:
            print(f'failed! => {proxy}')
    #
    #
    # 103.250.69.233:8080
    # 54.255.218.28:3128
    # 129.146.180.91:3128
    # 20.52.37.89:16379

    # proxies = {'http': 'http://20.52.37.89:16379',
    #            'https': 'https://20.52.37.89:16379'}

    # #
    # r = requests.get(
    #     'https://followerwonk.com/analyze/seekersoftec', proxies=proxies)
    # #
    # #
    # print(r.status_code)
    #
    #
