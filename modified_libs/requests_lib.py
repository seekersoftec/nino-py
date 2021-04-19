
#
from bs4 import BeautifulSoup
import sys
import random
import logging
import threading
import requests
#
from requests_futures.sessions import FuturesSession
#
from torpy.http.requests import tor_requests_session


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
# https://github.com/HOWZ1T/py_proxy
# PROXY
FILTERS = ["all", "au", "bd", "br", "by", "ca", "co", "cz", "de", "do", "ec", "eg", "es", "fr", "gb", "gr", "hk",
           "id", "il", "in", "it", "jp", "kr", "md", "mx", "nl", "ph", "pk", "pl", "ps", "ro", "ru", "se", "sg",
           "sy", "th", "tr", "tw", "ua", "us", "uz", "ve", "vn", "ye", "za", "zm"]


class Proxy:
    def __init__(self, country_code="all", validate_proxies=False):
        self.logger = logging.getLogger('py_proxy.proxy.Proxy')
        self.session = requests.Session()
        country_code = country_code.lower()

        is_valid = False
        for code in FILTERS:
            if country_code == code:
                is_valid = True
                break

        if is_valid:
            self.filter = country_code
        else:
            self.logger.info("bad filter given! country code: " +
                             country_code + " is not valid!\ndefaulting to no filter")
            self.filter = "all"

        self.index = 0
        self.proxies = self.fetch_proxies(self.filter)
        if len(self.proxies) <= 0:
            self.logger.error("no proxies found! try using the 'all' filter")
        else:
            self.proxy_count = len(self.proxies)
            self.proxy = self.format_proxy(self.proxies[self.index])

        self.valid_proxies = []
        # ready to be used with requests and validated.
        self.lock = threading.Lock()

        # giving start-up proxy validation control to the user
        if validate_proxies:

            if len(self.proxies) > 0:
                # validate and fill up the list
                self._thr_validate_proxies(chunksize=8)

    # allows the user to cycle through proxies
    def cycle(self, valid_only=False):
        if valid_only:
            if len(self.valid_proxies) > 0:
                idx = (self.index+1) % len(self.valid_proxies)
                prx = self.valid_proxies[idx]

                if prx is not None:
                    self.index = idx
                    self.proxy = self.format_proxy(prx)
                else:
                    self.logger.error(
                        "no valid proxies to cycle through! try the 'validate_proxies' method first.")
            else:
                self.logger.error(
                    "no valid proxies to cycle through! try the 'validate_proxies' method first.")
        else:
            self.index = (self.index+1) % self.proxy_count
            self.proxy = self.format_proxy(self.proxies[self.index])

    def fetch_proxies(self, country_="all"):
        country_ = country_.lower()

        is_valid = False
        for code in FILTERS:
            if country_ == code:
                is_valid = True
                break

        if not is_valid:
            self.logger.error("bad filter given! country code: " +
                              country_ + " is not valid!\ndefaulting to no filter")
            country_ = "all"

        self.logger.info("fetching proxies...")
        url = "https://free-proxy-list.net/"
        page = requests.get(url)

        if page.status_code != 200:
            self.logger.error(
                "Couldn't fetch proxies list! received bad response with code: " + str(page.status_code))
            sys.exit(1)
        else:
            self.logger.info("parsing data...")
            soup = BeautifulSoup(page.content, "html.parser")
            rows = soup.find_all("tr")

            proxies = []
            for row in rows:
                parts = row.find_all("td")
                if len(parts) == 8:
                    ip = parts[0].text
                    port = parts[1].text
                    country_code = parts[2].text
                    country = parts[3].text
                    provider = parts[4].text
                    google = parts[5].text
                    https = parts[6].text
                    last_checked = parts[7].text

                    if https == "yes" and (country_ == "all" or country_ == country_code.lower()):
                        proxies.append(
                            [ip, port, country_code, country, provider, google, https, last_checked])

            self.logger.info("retrieved " + str(len(proxies)) + " proxies")
            return proxies

    def validate_proxies(self, chunksize=8):
        if len(self.proxies) <= 0:
            self.logger.info("there are no proxies to validate.")
            return

        self.logger.info("validating proxies...")
        self._thr_validate_proxies(chunksize=chunksize)

    def _thr_test(self, proxy_):
        res = self.test_proxy(proxy_)
        if res == 1:
            self.lock.acquire()
            try:
                self.valid_proxies.append(proxy_)
            finally:
                self.lock.release()

    def _thr_multi_test(self, plist):
        for p in plist:
            self._thr_test(p)

    def _thr_validate_proxies(self, chunksize=8):
        def _chunks(l, n):
            for i in range(0, len(l), n):
                yield l[i:i+n]

        formatted_proxies = [self.format_proxy(p) for p in self.proxies]
        chunk_list = list(_chunks(formatted_proxies, chunksize))
        tlist = []

        for i in range(0, len(chunk_list)):
            task = threading.Thread(
                target=self._thr_multi_test, args=(chunk_list[i], ))
            tlist.append(task)
        for t in tlist:
            t.start()
        for t in tlist:
            t.join()

    @staticmethod
    def format_proxy(proxy):
        if isinstance(proxy, dict):  # checking if proxy is already formatted
            return proxy

        raw_ip_and_port = proxy[0] + ":" + proxy[1]
        http = "http://" + proxy[0] + ":" + proxy[1]
        https = "https://" + proxy[0] + ":" + proxy[1]
        proxy_dict = {
            "raw": raw_ip_and_port,
            "http": http,
            "https": https
        }
        return proxy_dict

    def test_proxy(self, proxy_, verbose=False):
        url = "https://www.iplocation.net/find-ip-address"
        if verbose:
            self.logger.info("testing proxy...")
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
                self.logger.info(
                    "\n\nSuccess! Able to connect with proxy\nConnection Details:\nip: " + ip + "\nlocation: " + location)
                self.logger.info("device: " + device + "\nos: " + os +
                                 "\nbrowser: " + browser + "\nuser agent: " + user_agent)
            return 1
        except requests.exceptions.ProxyError:
            if verbose:
                self.logger.error("request caused a proxy error!")
            return 0
        except AttributeError:
            if verbose:
                self.logger.error("Something went wrong.")
            return 0


#
#
#
def filter_proxies(proxies: list, time: str = 'seconds', https: str = 'yes'):
    #"IP Address\tPort\tCode\tCountry\tAnonymity\tGoogle\tHttps\tLast Checked\n"
    result = []
    for proxy in proxies:
        if ((time == None) or (https == None)):
            result.append(proxy)

        elif ((time in proxy[7]) and (proxy[6].lower() == https.lower())):
            result.append(proxy)

        else:
            pass
    #
    return result


#
#
#
def test_proxies(country: str = 'all'):
    proxy = Proxy()
    # proxies = filter_proxies(proxies=proxy.fetch_proxies('GB'), time='', https='')
    proxies_ = proxy.fetch_proxies(country_=country)
    #
    working_proxies = []
    #
    for i in range(len(proxies_)):
        # addr = [ip,port]
        addr = [proxies_[i][0], proxies_[i][1]]
        fmt_proxy = proxy.format_proxy(addr)
        del fmt_proxy['raw']
        # testing the current proxy
        try:
            res = proxy.test_proxy(fmt_proxy)
            if res == 1:
                print("success!")
                working_proxies.append(proxies_[i])
            else:
                print('failure!')
                pass
        except requests.exceptions.SSLError:
            pass
        #

        #
        print(fmt_proxy)

    return working_proxies


#
def get_working_proxies(list_range=100):
    proxy = Proxy()
    #
    working_proxies = []
    #
    for i in range(list_range):
        # getting the current proxy
        cur_proxy = proxy.proxy
        del cur_proxy['raw']
        # testing the current proxy
        try:
            res = proxy.test_proxy(cur_proxy)
            #
            if res == 1:
                print("success!")
                working_proxies.append(cur_proxy)
            else:
                print("failure!")
                pass
        except requests.exceptions.SSLError:
            pass

        # proxy.validate_proxies()
        #
        proxy.cycle()
        #
        print(cur_proxy)
    #
    return working_proxies


#
#
#
#
if __name__ == '__main__':
    # proxy = Proxy()
    # gets <country specific> only proxies from the pool
    # proxies = filter_proxies(
    #     proxies=proxy.fetch_proxies('GB'), time='', https='')
    # print(proxies)
    #
    #
    #
    # print('=> Getting working proxies...')
    # working_proxies = get_working_proxies()
    # working_proxies = test_proxies('us')
    # print('=> Done')
    # print(working_proxies)

    #
    #
    #
    # if (len(working_proxies) != 0):
    # proxies = working_proxies[random.randint(0, len(working_proxies)-1)]
    #
    proxies = {'http': 'http://54.255.218.28:3128',
               'https': 'https://54.255.218.28:3128'}
    #
    r = requests.get(
        'https://followerwonk.com/analyze/seekersoftec', proxies=proxies)
    #
    #
    print(r.status_code)
    #
    #
