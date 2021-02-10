# Collect_News
Collecting and grouping news with keyword.

# Environment
* Python 3.8
* requests 2.25.1
* bs4 0.0.1

# 기능
	- 뉴스 기사 크롤링
        네이버, 구글
    - 키워드 상세화
        입력받은 키워드를 의도에 맞는 형태로 상세화
            입력 키워드로 기사 목록 추출(관련도순?)
            목록에서 관련 기사 선택
            선택된 기사에서 상위 등장 키워드 추출
	- 동일 내용에 대한 중복 기사 그루핑
        Classification?
        n-gram 유사도
	- 결과 표출
        LINE notify 이용해서 신규 기사 발생 시 알림
    - 전체 수집된 목록 확인을 위한 페이지/문서 생성

# 플랫폼
	서버 + 라인 노티파이
	https://notify-bot.line.me/en/
	https://github.com/continu2720/granblue_ramge_bot/blob/master/bot_ramge.py
