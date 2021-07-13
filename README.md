# Collect_News
Collecting and grouping news with keywords.

---
## 플랫폼
PC/서버에서 기사 수집 및 메세지 발송.

---
## 기능
### 뉴스 기사 크롤링
NAVER 뉴스로부터 NAVER Open API를 이용한 기사 수집 구현.
  
### 키워드 상세화
수집하려는 대상 기사에 맞는 형태로 키워드 상세화.
* 키워드를 이용해 수집한 기사에서 제외할 기사 선택
* 선택/제외 정보를 이용한 관련/제외 키워드 추가
* 키워드 갱신 여부 확인

### 동일 내용에 대한 중복 기사 그루핑
n-gram cosine similarity를 이용한 Clustering 수행.

### 결과 표출
검색 결과 조회 및 신규 기사 그룹 발생 시 메세지 알림.

1. 조회 페이지 생성
2. Mail 발송
3. [LINE Notify](https://notify-bot.line.me/en/)
[https://github.com/continu2720/granblue_ramge_bot/blob/master/bot_ramge.py](https://github.com/continu2720/granblue_ramge_bot/blob/master/bot_ramge.py)

---

##TODO
1. Classify news on topic (main.py:search_news())
    1) load (selected/banned) news vectors
    2) classify the news
    3) add new group to result
2. CLI->GUI
3. Messaging
    * 웹페이지 생성 후 Mail 발송 
    * LINE Bot SDK 로 전환. https://github.com/line/line-bot-sdk-python