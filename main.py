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
    vector_json = {'selected': [], 'banned': []}

    for i in range(len(group_info)):
        if i in selected_groups['group']:
            selected_nouns_info.extend(nouns_info[i])

            # Save selected news vectors
            vector_json['selected'].append(nouns_info[i])
        else:
            vector_json['banned'].append(nouns_info[i])

    with open(configure.news_vector_filename, 'w+') as f:
        json.dump(vector_json, f)

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

            if i>0 and i%15 == 0:
                question[0]['message'] = f'Show more? ({i+1}/{cnt_sstr})'
                ans = prompt(question)
                if not ans['continue']:
                    break

    input('Press ENTER to return.')


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


if __name__ == '__main__':
    main()
