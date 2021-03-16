import requests
import configure


def send_line(msg: str) -> bool:
    """LINE notify 를 사용한 LINE 메세지 전송.
    https://notify-bot.line.me/en/
    https://github.com/continu2720/granblue_ramge_bot/blob/master/bot_ramge.py

    :param msg: 보낼 메세지
    :return: 메세지 전송 결과
    """
    res = False

    # For debug
    print(msg)
    return True

    # TODO: LINE Bot SDK 로 전환. https://github.com/line/line-bot-sdk-python

    try:
        TARGET_URL = 'https://notify-api.line.me/api/notify'
        TOKEN = configure.line_token
        response = requests.post(TARGET_URL,
                                 headers={'Authorization': 'Bearer ' + TOKEN},
                                 data={'message': msg})
        if response.status_code == 200:
            res = True
        else:
            print(res)
    except Exception as ex:
        print(ex)

    return res
