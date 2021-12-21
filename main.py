from bs4 import BeautifulSoup
import requests
import re

if __name__ == '__main__':

    KEYWORDS = ['дизайн', 'фото', 'web', 'python']
    KeyWords_string = '|'.join(KEYWORDS)
    pattern = re.compile(KeyWords_string, re.IGNORECASE)

    res = requests.get(url='https://habr.com/ru/all/')
    res.raise_for_status()
    soup = BeautifulSoup(res.text, features='html.parser')
    articles = soup.findAll('article')

    my_list = []

    for article in articles:

        article_title = article.find('a', class_='tm-article-snippet__title-link')
        all_article_text = article_title.text

        article_tags = article.find_all('a', class_='tm-article-snippet__hubs-item-link')
        if len(article_tags) > 0:
            for tag in article_tags:
                all_article_text += '\n' + tag.text

        article_text = article.find_all('p')
        if len(article_text) > 0:
            for paragraph in article_text:
                all_article_text += '\n' + paragraph.text

        href = article.find('a', class_='tm-article-snippet__title-link')

        res = re.findall(pattern, all_article_text)
        if len(res) > 0:
            print(f'{article.find("time")["title"]} - {article_title.text} - https://habr.com{href["href"]}')
        else:
            art_page = requests.get(url='https://habr.com' + href['href'], timeout=5)
            art_page.raise_for_status()
            a_soup = BeautifulSoup(art_page.text, features='html.parser')
            art_block = a_soup.find('article')
            a_res = re.findall(pattern, art_block.text)
            if len(a_res) > 0:
                # print(article_title.text)
                print(f'{article.find("time")["title"]} - {article_title.text} - https://habr.com{href["href"]}')