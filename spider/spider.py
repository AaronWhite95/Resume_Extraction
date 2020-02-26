from urllib.request import urlopen
from link_finder import LinkFinder
import re
from urllib.parse import urlparse
from domain import *
from general import *
import urllib.request
from urllib import parse
from bs4 import BeautifulSoup
import gzip
import random
import chardet
import ssl
try:
    from io import BytesIO as StringIO
except ImportError:
    try:
        from cStringIO import StringIO
    except ImportError:
        from StringIO import StringIO


class Spider:

    project_name = ''
    base_url = ''
    domain_name = ''
    queue_file = ''
    crawled_file = ''
    queue = set()
    crawled = set()

    def __init__(self, project_name, base_url, domain_name):
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.queue_file = Spider.project_name + '/queue.txt'
        Spider.crawled_file = Spider.project_name + '/crawled.txt'
        self.boot()
        #self.check_url(Spider.base_url)
        self.crawl_page('First spider', Spider.base_url)

    # Creates directory and files for project on first run and starts the spider
    @staticmethod
    def boot():
        create_project_dir(Spider.project_name)
        create_data_files(Spider.project_name, Spider.base_url)
        Spider.queue = file_to_set(Spider.queue_file)
        Spider.crawled = file_to_set(Spider.crawled_file)

    # Updates user display, fills queue and updates files
    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url not in Spider.crawled:
            print(thread_name + ' now crawling ' + page_url)
            print('Queue ' + str(len(Spider.queue)) + ' | Crawled  ' + str(len(Spider.crawled)))
            Spider.add_links_to_queue(Spider.gather_links(page_url))
            print("queue added")
            Spider.queue.remove(page_url)
            print("queue removed")
            Spider.crawled.add(page_url)
            print("crawled added")
            Spider.update_files()
            print("files updated")

    # Converts raw response data into readable information and checks for proper html formatting
    @staticmethod
    def gather_links(page_url):
        html_string = ''
        ssl._create_default_https_context = ssl._create_unverified_context
        my_headers = [
            "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0"
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
            "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)"
        ]
        Cookie = "; ".join(
            ["clientlanguage=zh_CN; UM_distinctid=16453b1bd8d0-00a81ded242d59-5b193413-100200-16453b1bd8e30b"])

        try:
            randdom_header = random.choice(my_headers)
            req = urllib.request.Request(page_url)
            req.add_header("User-Agent", randdom_header)
            #req.add_header("Host", "blog.csdn.net")
            req.add_header("Referer", "http://blog.csdn.net/")
            req.add_header("Cookie", Cookie)
            req.add_header("GET", page_url)
            response = urllib.request.urlopen(req)
            #response = urllib.request.urlopen(req).read().decode('utf-8')
            #response = urlopen(page_url)
            #if 'text/html' in response.getheader('Content-Type'):
            #    html_bytes = response.read()
            #    html_string = html_bytes.decode("utf-8")
            '''
            request = urllib.request.Request(page_url)
            request.add_header('Accept-encoding', 'gzip')
            request.add_header('Referer', 'https://www.baidu.com/')
            request.add_header('User-Agent',
                               'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36')
            response = urllib.request.urlopen(request)
            '''
            if response.info().get('Content-Encoding') == 'gzip':
                buf = StringIO( response.read())
                f = gzip.GzipFile(fileobj=buf)
                data = f.read()
            else:
                data = response.read()
            #print(data)
            chardit1 = chardet.detect(data)
            if chardit1['encoding'] == "utf-8" or chardit1['encoding'] == "UTF-8":
                data = data.decode('utf-8')
            else:
                data = data.decode('gbk')
            #print(data)
            soup = BeautifulSoup(data)
            arr_a = soup.find_all('a')
            links = set()
            for a in arr_a:
                value = a.get('href')
                new_value = str(value).replace(' ','')
                url = parse.urljoin(page_url, new_value)
                #url = parse.urljoin(page_url,value)
                links.add(url)
            #print(links)
            #html_string = data.decode("utf-8")
            #try:
            #    html_string = data.decode("utf-8")
            #except:
            #    html_string = data.decode("gbk")
            #finder = LinkFinder(Spider.base_url, page_url)
            #finder.feed(html_string)

        except Exception as e:
            print(str(e))

            return set()

        #return finder.page_links()
        return links

    # Saves queue data to project files
    @staticmethod
    def add_links_to_queue(links):
        for url in links:
            if (url in Spider.queue) or (url in Spider.crawled):
                continue
            #if Spider.domain_name != get_sub_domain_name(url):
            if get_sub_domain_name(url) not in Spider.domain_name:
                continue
            Spider.queue.add(url)

    @staticmethod
    def update_files():
        set_to_file(Spider.queue, Spider.queue_file)
        set_to_file(Spider.crawled, Spider.crawled_file)

    def check_url(self, url):
        request = urllib.request.Request(url)
        request.add_header('Accept-encoding', 'gzip')
        response = urllib.request.urlopen(request)
        if response.info().get('Content-Encoding') == 'gzip':
            buf = StringIO(response.read())
            f = gzip.GzipFile(fileobj=buf)
            data = f.read()
        else:
            data = response.read()
        soup = str(BeautifulSoup(data))
        if 'location.href' in soup:
            p = re.compile("location.href\s*=\s*\"(.*?)\";")
            new_url = p.findall(soup)
            domain = urlparse(url).netloc
            head = url.split(domain)[0]
            for i in range(len(new_url)):
                if 'http' not in new_url[i]:
                    new_url[i] = head + domain + new_url[i]
            Spider.add_links_to_queue(new_url)
