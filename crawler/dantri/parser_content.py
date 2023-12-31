import requests
from bs4 import BeautifulSoup
from requests import RequestException, Response

def get_connection(url: str, headers: dict, timeout=10):
    '''
    Get connection to web by url
    Args:
        * `url`: The url of web to crawl
        * `header`: Set header to requests, it helps avoid bot detection
        * `timeout`: The maximum of time to requests
    Return:
        * `response`: The response after requesting consists of *status_code*, *text* 
    '''
    reponse = requests.get(url=url, headers=headers, timeout=timeout)
    if reponse.status_code != 200:
        raise RequestException("The connection to this web has failed. Please try to connect again.")
    return reponse

def get_info_from_an_article(response: Response):
    info = {
        'title': None,
        'author': None,
        'time': None,
        'content': None
    }
    '''
    Get info from one news (title, author, ...)
    Args:
        * `response`: It's a response from an article
    Return:
        * `info`: The dictionary includes information from this article
    '''
    if response.status_code != 200:
        raise RequestException("Try to connect again.")
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
    