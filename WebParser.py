import csv
import urllib.request
import urllib.parse
import urllib.request
from operator import itemgetter

# import OldWebParser
import re

from bs4 import BeautifulSoup

from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter

# 그래프에 필요한 라이브러리를 불러옵니다.
import matplotlib.pyplot as plt

from wordcloud import WordCloud

from slack.web.classes import extract_json
from slack.web.classes.blocks import *


def make_wordcloud():
    text = open('./test.txt', 'r', encoding='UTF-8').read()

    import numpy as np
    from PIL import Image
    from wordcloud import STOPWORDS

    alice_mask = np.array(Image.open("./four-leaf.jpg"))

    stopwords = set(STOPWORDS)
    stopwords.add("said")

    wc = WordCloud(background_color="white", max_words=2000, mask=alice_mask, stopwords=stopwords)

    wc = wc.generate(text)

    plt.figure(figsize=(12, 12))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    plt.show()

    wc.to_file('cloud.png')

    # block3 = ImageBlock(
    #     image_url="./cloud.png",
    #     alt_text="I'm so sorryyyyyy"
    # )
    #
    # return  block3


# 그래프에 필요한 라이브러리를 불러옵니다.
import matplotlib.pyplot as plt

from wordcloud import WordCloud

from slack.web.classes import extract_json
from slack.web.classes.blocks import *


SLACK_TOKEN = ""
SLACK_SIGNING_SECRET = ""

app = Flask(__name__)
# /listening 으로 슬랙 이벤트를 받습니다.
slack_events_adaptor = SlackEventAdapter(SLACK_SIGNING_SECRET, "/listening", app)
slack_web_client = WebClient(token=SLACK_TOKEN)



def info_Haezone(list_info):
    # list_text = '1996/10/09/14:00/양력/여'
    # list_info = list_text.strip().split("/")
    info = {}
    info['year'] = list_info[0]  # 1960 ~ 1999
    info['month'] = list_info[1]  # 1 ~ 12
    info['day'] = list_info[2]  # 1 ~ 29
    # info['time'] = list_info[3].split(":")  # 24시간 = 1440분
    # info['time'] = int(info['time'][0]) * 60 + int(info['time'][1])
    info['time'] = int(list_info[3][0:2]) * 60 + int(list_info[3][3:5])

    if info['time'] in range(0, 91):
        info['time'] = '0'  # 00:00 - 01:30
    elif info['time'] in range(91, 211):
        info['time'] = '2'  # 01:31 - 03:30
    elif info['time'] in range(211, 331):
        info['time'] = '4'
    elif info['time'] in range(331, 451):
        info['time'] = '6'
    elif info['time'] in range(451, 571):
        info['time'] = '8'
    elif info['time'] in range(571, 691):
        info['time'] = '10'
    elif info['time'] in range(691, 811):
        info['time'] = '12'
    elif info['time'] in range(811, 931):
        info['time'] = '14'
    elif info['time'] in range(931, 1051):
        info['time'] = '16'
    elif info['time'] in range(1051, 1171):
        info['time'] = '18'
    elif info['time'] in range(1171, 1291):
        info['time'] = '20'
    elif info['time'] in range(1291, 1411):
        info['time'] = '22'
    elif info['time'] in range(1411, 1441):
        info['time'] = '24'

    if list_info[4] == '양력':
        info['lunar'] = '0'
    elif list_info[4] == '음력':
        info['lunar'] = '1'
    elif list_info[4] == '윤달':
        info['lunar'] = '2'

    # 양력/음력/윤달
    if list_info[5] == '남':
        info['sex'] = 'M'
    elif list_info[5] == '여':
        info['sex'] = 'F'
    else:
        info['sex'] = list_info[5]

    return info


def info_Unsesin(list_info):
    # list_text = '1996/10/09/14:00/양력/여'
    # list_info = list_text.strip().split("/")

    info = {}
    info['year'] = list_info[0]  # 1960 ~ 1999
    info['month'] = int(list_info[1])  # 1 ~ 12
    if info['month'] in range(1, 9): info['month'] = '0' + str(info['month'])
    info['month'] = str(info['month'])
    info['day'] = int(list_info[2])  # 1 ~ 29
    if info['day'] in range(1, 9): info['day'] = '0' + str(info['day'])
    info['day'] = str(info['day'])
    if list_info[3] == '모름':
        info['time'] = '0'
    else:
        list_info[3].split(":")  # 24시간 = 1440분
        info['time'] = int(list_info[3][0:2]) * 60 + int(list_info[3][3:5])
        if info['time'] in range(0, 90):
            info['time'] = '01'  # 00:00 - 01:30
        elif info['time'] in range(90, 210):
            info['time'] = '02'  # 01:31 - 03:30
        elif info['time'] in range(210, 330):
            info['time'] = '04'
        elif info['time'] in range(330, 450):
            info['time'] = '06'
        elif info['time'] in range(450, 570):
            info['time'] = '08'
        elif info['time'] in range(570, 690):
            info['time'] = '10'
        elif info['time'] in range(690, 810):
            info['time'] = '12'
        elif info['time'] in range(810, 930):
            info['time'] = '14'
        elif info['time'] in range(930, 1050):
            info['time'] = '16'
        elif info['time'] in range(1050, 1170):
            info['time'] = '18'
        elif info['time'] in range(1170, 1290):
            info['time'] = '20'
        elif info['time'] in range(1290, 1410):
            info['time'] = '22'
        elif info['time'] in range(1410, 1441):
            info['time'] = '01'

    # 양력/음력/윤달
    if list_info[4] == '양력':
        info['lunar'] = 'S_C'
    elif list_info[4] == '음력':
        info['lunar'] = 'L_C'
    elif list_info[4] == '윤달':
        info['lunar'] = 'L_L'

    if list_info[5] == 'M':
        info['sex'] = '남'
    elif list_info[5] == 'F':
        info['sex'] = '여'
    else:
        info['sex'] = list_info[5]

    return info


def info_Yuksul(list_info):
    # list_text = '1996/10/09/14:00/양력/여'
    # list_info = info_text.strip().split("/")

    info = {}
    info['year'] = list_info[0]  # 1960 ~ 1999
    info['month'] = list_info[1]  # 1 ~ 12
    info['day'] = list_info[2]  # 1 ~ 29
    # info['time'] = list_info[3].split(":")  # 24시간 = 1440분
    # info['time'] = int(list_info[3][0:2]) * 60 + int(list_info[3][3:5])
    info['hour'] = list_info[3][0:2]
    info['minute'] = int(list_info[3][3:5])
    if info['minute'] == 0:
        info['minute'] = '0'
    if info['minute'] in range(1, 10):
        info['day'] = str(info['day']).replace('0', '')
    info['minute'] = str(info['minute'])

    if list_info[4] == '양력':
        info['lunar'] = '2'
    elif list_info[4] == '음력':
        info['lunar'] = '1'
    elif list_info[4] == '윤달':
        info['lunar'] = '3'
    # 양력/음력/윤달
    if list_info[5] == '남' or list_info[5] == 'M':
        info['sex'] = '1'
    elif list_info[5] == '여' or list_info[5] == 'F':
        info['sex'] = '2'

    return info


# http://shinhan.haezone.com/
def parsingHaezone(info):
    info = info_Haezone(info)
    ### urllib 에서 POST 데이터 전송방법
    ### 참고사이트 : https://comsecuodj.tistory.com/59
    post_data = urllib.parse.urlencode(
        {'cp_file': '', 'bType': 'A027', 'bMinute': '00', 'email': '', 'gopaymethod': '', 'price': '0',
         'bCounting_A027': '', 'referer': '', 'add1': '', 'UserNM': 'Alice', 'bLunar': info['lunar'],
         'bSex': info['sex'],
         'bYear': info['year'], 'bMonth': info['month'], 'bDay': info['day'], 'bHour': info['time'], 'x': '69',
         'y': '12'}).encode('EUC-KR')
    url = urllib.request.Request("http://shinhan.haezone.com/GoodLuck.asp", post_data)
    url.add_header("User-Agent", 'Mozilla/5.0 (Windows NT 6.1; Win64; x64')

    source_code = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(source_code, "html.parser")

    temp = []
    output = []
    for i in soup.find_all("div", class_="res_section"):
        temp.append(i.get_text().strip().split('\n'))

    output.append(temp[1][-1])
    output.append(temp[2][0])
    output.append(temp[3][0])
    output.append(temp[4][0])
    output.append(temp[5][0])
    output.append(temp[6][0])

    return output[1:6]


# http://unse.sportschosun.com/unse/free/today/result
def parsingUnsesin(info):
    info = info_Unsesin(info)
    # info = OldWebParser.info_Unsesin(info)
    ### urllib 에서 POST 데이터 전송방법
    ### 참고사이트 : https://comsecuodj.tistory.com/59

    # 월/일 2글자 처리
    if len(str(info['month'])) == 1:
        info['month'] = '0' + str(info['month'])

    if len(str(info['day'])) == 1:
        info['day'] = '0' + str(info['day'])

    # print(info['month'])
    # print(info['day'])

    # post = {'target_yyyy': '2019', 'user_name': 'Alice', 'sex': '남' , 'birth_yyyy': info['year'], 'birth_mm': info['month'],
    #      'birth_dd': info['day'], 'birth_hh': '08', 'birth_solunar': 'S_C'}

    post_data = urllib.parse.urlencode(
        {'target_yyyy': '2019', 'user_name': 'Alice', 'sex': info['sex'], 'birth_yyyy': info['year'],
         'birth_mm': info['month'],
         'birth_dd': info['day'], 'birth_hh': info['time'], 'birth_solunar': info['lunar']}).encode('UTF-8')
    # post_data = urllib.parse.urlencode(post).encode('UTF-8')
    url = urllib.request.Request("http://unse.sportschosun.com/unse/free/today/result", post_data)
    url.add_header("User-Agent", 'Mozilla/5.0 (Windows NT 6.1; Win64; x64')

    source_code = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(source_code, "html.parser")

    temp = []
    output = []

    temp.append(soup.find("div", class_="today_result"))
    for i in soup.find("div", class_="today_result02").find_all("div"):
        temp.append(i.get_text().strip().split('\n'))

    # print(temp)
    # num = 0
    # for i in temp:
    #     print(num, end='')
    #     print(i)
    #     num = num+1
    # output.append(temp[0][2])
    # output.append(temp[0][3])
    output.append(temp[1][1])
    output.append(temp[2][1])
    output.append(temp[3][1])
    output.append(temp[4][1])
    output.append(temp[5][1])
    return output


# http://www.yuksul.com/saju/regular_today.asp
def parsingYuksul(info):
    info = info_Yuksul(info)
    ### urllib 에서 POST 데이터 전송방법
    ### 참고사이트 : https://comsecuodj.tistory.com/59
    # print(info)
    post_data = urllib.parse.urlencode(
        {'code': '1',
         'file_prefix': '',
         'url_root': 'http://www.yuksul.com/',
         'Diffday': info['lunar'],
         'year': info['year'],
         'month': info['month'],
         'day': info['day'],
         'hour': info['hour'],
         'minute': info['minute'],
         'sex': info['sex']}).encode('UTF-8')
    url = urllib.request.Request("http://www.yuksul.com/saju/regular_today.asp", post_data)
    url.add_header("User-Agent", 'Mozilla/5.0 (Windows NT 6.1; Win64; x64')

    source_code = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(source_code, "html.parser")

    temp = []
    output = []
    for i in soup.find_all("td"):
        temp.append(i.get_text().strip().replace('\n', ''))

    output.append(temp[15])  # 종합결과
    output.append(temp[20])  # 사업결과
    output.append(temp[25])  # 금전결과
    output.append(temp[30])  # 이성결과

    return output


def parsingAll():
    return [parsingHaezone, parsingUnsesin, parsingYuksul]


def _crawl_unse(text):
    text = text.replace("<@UKY8U83CK>", '').strip()
    # info_text = '1996/01/09/14:00/양력/여'
    if re.match('^[0-9]{4}/[0-9]{2}/[0-9]{2}/[0-9]{2}:[0-9]{2}/[가-힣]{2}/[가-힣]{1}$', text):
        pass
    else:
        return "`@<봇이름> 년도(4)/월(2)/일(2)/시(2):분(2)/양력 or 음력 or 윤달/남 or 여` 형식으로 입력해주세요!" + "\n`ex)@yeseul_bot 1996/01/09/14:00/양력/여`"

    info = text.strip().split("/")

    output = []

    # output.append("옜다 운세\n\n")
    for data in parsingHaezone(info):
        output.append(data)
    # output.append("\n\n\n나는야 운세의 신\n\n")
    for data in parsingUnsesin(info):
        output.append(data)
    # output.append("\n\n\n나는야 역술의 신\n\n")
    for data in parsingYuksul(info):
        output.append(data)

    output = '.'.join(output)
    rank = sentenceScoring(output)
    rank = list(map(itemgetter(0),rank))

    text = '\n\n'.join(rank[0:3])
    f = open("test.txt", 'w',  encoding='utf8')
    f.write(text)
    f.close()

    return '\n\n'.join(rank[0:3])

    # return '.'.join(output)


def sentenceScoring(rawString):
    with open('LuckScore.csv') as scoreFile:
        wordScore = []
        reader = csv.reader(scoreFile, delimiter=',')
        for row in reader:
            wordScore.append([row[0], int(row[1])])

    rankedList = []
    unrankedList = rawString.split('.')

    # print(unrankedList)

    for sentence in unrankedList:
        if sentence == '':
            continue
        else:
            score = 0
            for word in wordScore:
                if word[0] in sentence:
                    score = score + word[1]
            rankedList.append([sentence, score])

    rankedList = sorted(rankedList, key=itemgetter(1), reverse=True)

    # 랭킹 확인하는 코드
    # for i in rankedList:
    #     print(i)

    return rankedList


# 챗봇이 멘션을 받았을 경우
@slack_events_adaptor.on("app_mention")
def app_mentioned(event_data):
    channel = event_data["event"]["channel"]
    text = event_data["event"]["text"]

    # 리턴타입이 리스트입니다. 좋은운은 [:n], 나쁜운은 [-n:] 으로 확인해주세요
    message = _crawl_unse(text)

    make_wordcloud()
    # block3 = make_wordcloud()
    # my_blocks = [block3]

    slack_web_client.chat_postMessage(
        channel=channel,
        text= "당신의 하루에 늘어붙은 행운:\n\n" + message
        # blocks = extract_json(my_blocks)
    )


# / 로 접속하면 서버가 준비되었다고 알려줍니다.
@app.route("/", methods=["GET"])
def index():
    return "<h1>Server is ready.</h1>"


if __name__ == '__main__':
    app.run('127.0.0.1', port=4040)
