import requests
from bs4 import BeautifulSoup


class ProxyInfo:
    ip_addr: str
    port: int
    is_https: bool


class ProxyScraping:

    def __init__(self):
        self.url = "https://free-proxy-list.net/"
        self.request = requests.get(self.url)
        self.proxies = []

    def update_proxies(self):
        pass
        "/html/body/section[1]/div/div[2]/div/div[2]/div/table/tbody/tr[1]"

    def get_proxies(self, nb_proxy):
        pass


proxies = {
 "http": "http://85.10.219.99:1080",
 "https": "http://188.40.183.190:1080",
}

proxies = {
 "http": "http://178.128.197.137:8080",
 "https": "http://188.40.183.190:1080",
}

proxies = {
 "http": "http://85.10.219.99:1080",
 # "https": "http://188.40.183.190:1080",
}

r = requests.get("http://quotes.toscrape.com/", proxies=proxies)
print(r.content)
