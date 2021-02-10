from collect import collect_naver


def run():
    # search_keyword = 'SEARCH-KEYWORD-TO-SEARCH'
    search_keyword = '비비'

    # Collect news from NAVER news.
    news_info = collect_naver(search_keyword)

    # Extract related words.
    # keywords = extract_keywords(news_info)

    # send LINE notify and select keywords

    # classify news on topic

    # send LINE notify


if __name__ == '__main__':
    run()
