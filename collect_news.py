import requests
from bs4 import BeautifulSoup
from time import sleep

import configure


def collect_naver(keyword: str, lastcheck: int=None) -> list:
    return collect_naver_v2(keyword, lastcheck)


def collect_naver_v2(keyword: str, lastcheck: int=None) -> list:
    """NAVER 뉴스에서 keyword로 기사를 검색하고 결과를 리턴함.

    :param keyword: 검색 키워드
    :param lastcheck: 마지막 확인한 시간
    :return: 기사 정보 list. [{title, desc, url},]
    """
    collect_result = []

    search_url = f'https://openapi.naver.com/v1/search/news.json?query={keyword}&display=100'
    search_option = '&start='

    request_header = {
        'X-Naver-Client-Id': configure.naver_openapi_id,
        'X-Naver-Client-Secret': configure.naver_openapi_secret
    }
    for start_num in range(10):
        if start_num > 0:
            requrl = search_url + search_option + str(start_num*100+1)
        else:
            requrl = search_url

        res = requests.get(requrl, headers=request_header)
        if res.status_code != 200:
            return

        news_list = res.json()

        for news in news_list['items']:
            collect_result.append({
                'title': news['title'],
                'desc': news['description'],
                'url': news['link'],
                'pubDate': news['pubDate']
            })

        if len(news_list) < 100:
            break

        sleep(0.2)

    return collect_result


def collect_naver_v1(keyword: str, lastcheck: int=None) -> list:
    """NAVER 뉴스에서 keyword로 기사를 검색하고 결과를 리턴함.

    :param keyword: 검색 키워드
    :param lastcheck: 마지막 확인한 시간
    :return: 기사 정보 list. [{title, desc, url},]
    """
    collect_result = []

    search_url = f'https://search.naver.com/search.naver?&where=news&sort=1&query={keyword}'
    search_option = '&start='

    for start_num in range(10):
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

        sleep(0.2)

    return collect_result


def collect_google(keyword: str) -> list:
    """*작성중*Google 뉴스로부터 정보 수집.

    :param keyword:
    :return:
    """
    collect_result = []

    return collect_result


def get_bs_obj(url: str) -> BeautifulSoup:
    page = requests.get(url)
    bs_obj = BeautifulSoup(page.content, 'html.parser')

    return bs_obj
