#-*-coding:utf-8 -*-
import threading
from queue import Queue
from spider import Spider
from domain import *
from general import *

num = 1
#filename = input('please input the input filename' + '\n' + '[for example, ]:'+ '\n')
#filename = 'E:/桌面的东西/情报所/project/北理工识别人员简历/1-爬取所有子链接/源码/源码/input.txt'
filename = 'input.txt'
f = open(filename)

#print num
#print line
lines = f.readlines()
HOMEPAGE = lines[0].strip()
print('crawling the website:' + HOMEPAGE)
#print HOMEPAGE
#PROJECT_NAME = 'linksfolder_' + str(num)
PROJECT_NAME = lines[1]
#print PROJECT_NAME
#print type(PROJECT_NAME)
DOMAIN_NAME = get_sub_domain_name(HOMEPAGE)
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
NUMBER_OF_THREADS = 8
queue = Queue()
Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)

# Create worker threads (will die when main exits)
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# Do the next job in the queue
def work():
    while True:
        url = queue.get()
        Spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()


# Each queued link is a new job
def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join()
    crawl()


# Check if there are items in the queue, if so crawl them
def crawl():
    queued_links = file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        print(str(len(queued_links)) + ' links in the queue')
        create_jobs()


create_workers()
crawl()
num += 1

