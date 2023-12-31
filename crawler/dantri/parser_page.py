import time
from tqdm import tqdm
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from collections import defaultdict
from .utils import check_is_next_page_from_root, get_connection

def get_topics(root_url: str, headers: dict, timeout=10):
    '''
    Extract the main topics from website.
    
    Args:
        * `root_url`: Home page of web
        * `header`: Set header to requests, it helps avoid bot detection
        * `timeout`: The maximum of time to requests
        
    Return:
        * `topics`: the dictionary of main topics and each main topic has children
    '''
    response = get_connection(root_url, headers, timeout)
    topics = defaultdict(dict)
    soup = BeautifulSoup(response.text, "lxml")
    menu_ol = soup.find('ol', class_='menu-wrap')
    topic_li = menu_ol.find_all('li', class_='has-child')
    for topic in topic_li:
        a_tags = topic.find_all('a', href=True)
        main_topic_name = a_tags[0].text
        sub_topic_links = [urljoin(root_url, a_tag['href']) for a_tag in a_tags[1:] if check_is_next_page_from_root(a_tag['href'])]
        topics[main_topic_name] = sub_topic_links
    return topics

def get_articles_by_topic(topic_url: str, headers: dict, timeout=10, max_pagination=5):
    if max_pagination <= 0:
        raise ValueError("MAX_PAGINATION must be positive")
    
    articles_links = []
    next_page = topic_url
    for _ in tqdm(range(max_pagination)):
        response = get_connection(next_page, headers, timeout)
        soup = BeautifulSoup(response.text, 'lxml')
        articles = soup.find_all('article', class_='article-item')
        articles_links += [urljoin(topic_url, article.find('a')['href']) for article in articles]
        
        has_next = soup.find('a', class_='next')
        if has_next == None:
            break
        next_page = urljoin(topic_url, has_next['href'])
        time.sleep(1)
    
    return articles_links

def get_info_from_an_article(article_url: str, headers: dict, timeout=10):
    '''
    Get info from one news (title, author, ...)
    
    Args:
        * `response`: It's a response from an article
        
    Return:
        * `info`: The dictionary includes information from this article
    '''
    
    info = {
        'title': None,
        'author': None,
        'time': None,
        'content': None
    }
    response = get_connection(article_url, headers, timeout)
    soup = BeautifulSoup(response.text, 'lxml')
    container = soup.find('article', class_='singular-container')
    
    if container is None:
        return info
    
    h1 = container.find('h1')
    title = h1.text if h1 is not None else None
    info['title'] = title
    
    author_name_div = container.find('div', class_='author-name')
    author = author_name_div.text if author_name_div is not None else None
    info['author'] = author
    
    author_time_div = container.find('time', class_='author-time')
    author_time = author_time_div['datetime'] if author_time_div is not None else None
    info['time'] = author_time
    
    content_div = container.find('div', class_='singular-content')
    
    if content_div != None:
        content_list = [content.text for content in content_div.find_all('p')]
        content = ' '.join(content_list)
        info['content'] = content
    return info
    