# -*- coding: utf-8 -*-

from collect_news import collect_naver
from analyze_news import extract_keywords, classify_news
from line_notify import send_line
import configure

from PyInquirer import prompt
import json


def search_news():
    # Read searching keywords from file
    with open(configure.search_string_filename, 'r') as f:
        search_strings = f.readlines()

    for search_str in search_strings:
        # Collect news from NAVER news.
        news_info = collect_naver(search_str, int)

        # Classify news on topic
        # TODO: 1) load (selected/banned) news vectors, 2) classify the news, 3) add new group to result

        # Make message
        line_msg = '\n'
        for i in range(len(news_info)):
            title = news_info[i]['title']
            line_msg += f'{i}. {title}\n'

        # Send LINE notify
        send_line(line_msg)


def add_monitor():
    # Get new keyword
    wait_input = True
    question = [{
        'type': 'confirm',
        'name': 'chk_input',
        'message': '[] Right?',
        'default': True
    }]
    while wait_input:
        new_keyword = input('Write new keyword to search: ')
        question[0]['message'] = f'[{new_keyword}] Right?'
        chk_input = prompt(question)
        wait_input = not chk_input['chk_input']

    # Collect news from NAVER news.
    news_info = collect_naver(new_keyword, int)

    # Classify news
    group_info, nouns_info = classify_news(news_info)

    # Show list of news
    group_list = [
        {
            'type': 'checkbox',
            'name': 'group',
            'message': 'Select every news what you want',
            'choices': [
            ]
        }
    ]
    for i in range(len(group_info)):
        group_list[0]['choices'].append({
            'value': i,
            'name': news_info[group_info[i][0][0]]['title']
        })

    selected_groups = prompt(group_list)

    # Extract related words from selected news groups.
    selected_nouns_info = []
    vectors = {'selected': [], 'banned': []}

    for i in range(len(group_info)):
        if i in selected_groups['group']:
            selected_nouns_info.extend(nouns_info[i])

            vectors['selected'].extend(nouns_info[i])
        else:
            vectors['banned'].extend(nouns_info[i])

    save_nouns_vector(vectors)

    selected_keywords = extract_keywords(selected_nouns_info)
    selected_keywords = list(set(selected_keywords))

    # Select search keywords
    keyword_list = [
        {
            'type': 'checkbox',
            'name': 'keyword',
            'message': 'Select every keywords what you want',
            'choices': [
            ]
        }
    ]
    for i in range(len(selected_keywords)):
        keyword_list[0]['choices'].append({
            'checked': True,
            'name': selected_keywords[i]
        })

    selected_items = prompt(keyword_list)

    # Save search strings
    new_search_str = ' '.join(selected_items['keyword'])

    with open(configure.search_string_filename, 'w+') as f:
        search_strings = f.readlines()
        search_strings.append(new_search_str)
        search_strings = list(set(search_strings))
        f.writelines(search_strings)

    print(f'Keyword Added: {search_strings}')
    input('Press ENTER to return.')


def show_monitors():
    with open(configure.search_string_filename, 'r') as f:
        search_strings = f.readlines()

    cnt_sstr = len(search_strings)

    if cnt_sstr == 0:
        print('No Monitors.')
    else:
        question = [
            {
                'type': 'confirm',
                'message': 'Show more?',
                'name': 'continue',
                'default': True
            }
        ]

        for i in range(cnt_sstr):
            print(search_strings[i])

            if i > 0 and i % 15 == 0:
                question[0]['message'] = f'Show more? ({i + 1}/{cnt_sstr})'
                ans = prompt(question)
                if not ans['continue']:
                    break

    input('Press ENTER to return.')


def save_nouns_vector(vectors: dict):
    nouns_dict = dict()

    new_vec = dict()
    for grp in ['selected', 'banned']:
        new_grp = []
        for news in vectors[grp]:
            new_news = dict()
            for k, v in news.items():
                if k in nouns_dict:
                    index = nouns_dict[k]
                else:
                    index = len(nouns_dict)
                    nouns_dict[k] = index
                new_news[index] = v
            new_grp.append(new_news)
        new_vec[grp] = new_grp

    with open(configure.nouns_dict_filename, 'w+') as f:
        # Save news vectors
        json.dump(nouns_dict, f)

    with open(configure.news_vector_filename, 'w+') as f:
        # Save news vectors
        json.dump(new_vec, f)


def load_nouns_vector() -> (dict, list):
    nouns_dict = []

    with open(configure.nouns_dict_filename, 'r') as f:
        json_dict = json.load(f)

        for k, v in nouns_dict.items():
            nouns_dict.append(k)

    vectors = dict()
    with open(configure.news_vector_filename, 'r') as f:
        json_dict = json.load(f)

        for grp in ['selected', 'banned']:
            new_grp = []
            for news in json_dict[grp]:
                new_news = dict()
                for k, v in news.items():
                    new_news[nouns_dict[k]] = v
                new_grp.append(new_news)
            vectors[grp] = new_grp

    return vectors, nouns_dict


def main():
    questions = [
        {
            'type': 'list',
            'name': 'menu_entry',
            'message': 'Select what to do.',
            'choices': [
                {
                    'key': '1',
                    'name': 'Add new monitor',
                    'value': '1'
                },
                {
                    'key': '2',
                    'name': 'Show current monitors',
                    'value': '2'
                },
                {
                    'key': '3',
                    'name': 'Monitoring start',
                    'value': '3'
                },
                {
                    'key': 'q',
                    'name': 'Quit',
                    'value': 'q'
                }
            ]
        }
    ]
    while True:
        menu_entry = prompt(questions)
        menu_entry = menu_entry['menu_entry']

        if menu_entry == '1':
            add_monitor()
        elif menu_entry == '2':
            show_monitors()
        elif menu_entry == '3':
            search_news()
        elif menu_entry == 'q':
            break


from analyze_news import extract_nouns


def test():
    teststr = (
        '특히 디지털 런웨이 영상 기획부터 디자이너가 적극 참여해 시즌 컨셉에 맞는 연출을 이끌었으며, 음악, 예술 분야 아티스트와의 협력으로 화제성은 물론 대중성까지 더했다.'
        '▲얼킨은 ‘투모로우바이투게더(TOMORROW X TOGETHER, 빅히트 엔터테인먼트 소속)’ 멤버 연준과 뮤지션 ‘비비(BIBI, 필굿뮤직 소속)’가 런웨이 모델로 등장하며, ▲자렛은 중국 그룹 ‘웨이션브이(WayV, SM엔터테인먼트 소속)’멤버 양양과 협업하는 등 K-팝과 K-패션의 결합을 통해 참가 브랜드의 매력 알리기에 나선다. 또한, ▲분더캄머는 국내 굴지의 프로덕션 ‘매스메스에이지’와 협업으로 한 편의 영화를 보는 듯한 런웨이 영상을 보여줄 예정이다.'
    )
    res = extract_nouns(teststr)

    print(res)


if __name__ == '__main__':
    main()
    # test()
