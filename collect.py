import requests
from bs4 import BeautifulSoup


def collect_naver(keyword: str) -> list:
    """
    NAVER 뉴스에서 keyword로 기사를 검색하고 결과를 리턴함.
    :param keyword: 검색 키워드
    :return: 기사 정보 list. [{title, desc, url}]
    """
    collect_result = []

    search_url = f'https://search.naver.com/search.naver?&where=news&sort=1&query={keyword}'
    search_option = '&start='

    for start_num in range(3):
        if start_num > 0:
            bs_obj = get_bs_obj(search_url + search_option + str(start_num*10+1))
        else:
            bs_obj = get_bs_obj(search_url)

        news_list = bs_obj.find_all('div', {'class': 'news_area'}, limit=10)

        for news in news_list:
            title = news.find('a', {'class': 'news_tit'}).text
            desc = news.find('a', {'class': 'dsc_txt_wrap'}).text
            url = news.div.a.href

            collect_result.append({'title': title, 'desc': desc, 'url': url})

        if len(news_list) < 10:
            break

    return collect_result


def collect_google(keyword: str) -> list:
    collect_result = []

    return collect_result


def get_bs_obj(url: str) -> BeautifulSoup:
    page = requests.get(url)
    bs_obj = BeautifulSoup(page.content, 'html.parser')

    return bs_obj
