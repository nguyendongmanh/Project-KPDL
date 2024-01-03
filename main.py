import time
import json
from tqdm import tqdm
from config import Config
from crawler import dantri
from collections import defaultdict

HOST = Config.HOST
PORT = Config.PORT
DB_NAME = Config.DB_NAME
COLLECTION_NAME = Config.COLLECTION_NAME
ROOT_URL = Config.ROOT_URL
HEADERS = Config.HEADERS
TIMEOUT = Config.TIMEOUT
TARGET = Config.TARGET
MAX_PAGINATION = Config.MAX_PAGINATION
EXPORT_TO = Config.EXPORT_TO

def get_all_from_dantri(root_url: str, headers: dict, timeout=10):
    dantri.check_time_out(timeout)
    
    topics = dantri.get_topics(root_url=root_url, headers=headers, timeout=timeout)
    # get all article's link in each pagination
    articles_by_topic = defaultdict(list)
    for main_topic, sub_topics in topics.items():
        print(main_topic)
        for sub_topic in sub_topics:
            articles_links = dantri.get_articles_by_topic(sub_topic, headers=headers, timeout=timeout, max_pagination=MAX_PAGINATION)
            articles_by_topic[main_topic] += articles_links
            time.sleep(1)
        time.sleep(1)
    
    # get article's information    
    articles_content_by_topic = defaultdict(list)
    for topic, articles in articles_by_topic.items():
        print(topic)
        for article_link in tqdm(articles):
            articles_content_by_topic[topic].append(dantri.get_info_from_an_article(article_link, headers=headers, timeout=timeout))
            time.sleep(0.5)
        time.sleep(1)
    
    file_type = EXPORT_TO.lower()
    
    if file_type == 'json':
        # write output to json
        with open('data/dantri.json', "w", encoding='utf-8') as f:
            json.dump(articles_content_by_topic, f, indent=4, ensure_ascii=False)
    elif file_type == 'csv':
        pass
    elif file_type == 'mongo':
        pass
    else:
        raise Exception("You only can save data as 2 type, json and csv")

def get_all_from_vnexpress(root_url: str, headers: dict, timeout=10):
    pass

def main():
    if TARGET == 'dantri':
        get_all_from_dantri(ROOT_URL, HEADERS, TIMEOUT)
    elif TARGET == 'vnexpress':
        get_all_from_vnexpress(ROOT_URL, HEADERS, TIMEOUT)

if __name__ == '__main__':
    main()
    
