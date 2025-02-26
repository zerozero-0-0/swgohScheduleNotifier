import requests
from datetime import datetime
from bs4 import BeautifulSoup

# 現在時刻を取得
current_time = datetime.now()

months = ["january", "february", "march", "april", "may", "june", 
          "july", "august", "september", "october", "november", "december"]

month = current_time.month
month = months[month - 1]
year = current_time.year

url = f"https://www.ea.com/ja-jp/games/starwars/galaxy-of-heroes/news/{month}-calendar-preview-{year}"


res = requests.get(url)

if res.status_code == 200:
    data =  res.text

soup = BeautifulSoup(data, "html.parser")

data = []

elements = soup.find_all("ea-text")

for element in elements:
    text = element.text
    lines = text.split("\n")
    for line in lines:
        if line != "":
            data.append(line)


def isAllElementIsPresent(EventType, EventName, EventDate) :
    if(EventType == "" or EventName == "" or EventDate == ""):
        return False
    else:
        return True



EventTypes = ["オメガイベント", "アサルトバトル", "神話イベント", "艦隊マスター", "テリトリーバトル", "テリトリーウォーズ"]

events = []

index = -1


EventType = ""
EventName = ""
EventDate = ""

for eachData in data:
    if eachData == "ホーム・ワン、エグゼキュートリクス、エンデュアランス、ラダス、ファイナライザーは、注目のシップの設計図を330個持っていないプレイヤーのためのデイリーイベントになりました。":
        continue
    updated = False
    if index + 1 < len(EventTypes) and eachData == EventTypes[index + 1]:
        index += 1
        EventType = EventTypes[index]
    elif EventType == "":
        continue
    elif EventName == "":
        EventName = eachData
    elif EventDate == "":
        EventDate = eachData


    if index == -1:
        continue
    else:
        if isAllElementIsPresent(EventType, EventName, EventDate) == True:
            events.append({
                "EventType": EventType,
                "EventName": EventName,
                "EventDate": EventDate
            })
            updated = True
    
    if updated:
        EventName = ""
        EventDate = ""
        updated = False


for event in events:
    print(event)