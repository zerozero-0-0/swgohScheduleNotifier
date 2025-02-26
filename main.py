import discord
from discord.ext import commands
import schedule
import time
from datetime import datetime
import requests
import asyncio
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from bs4 import BeautifulSoup
import os

JST = ZoneInfo("Asia/Tokyo")


TOKEN = os.getenv('DISCORD_BOT_TOKEN')

CHANNEL_ID = os.getenv('CHANNEL_ID')

Hour = 6
Minute = 0
Second = 0


current_time = datetime.now()


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

def index():
    months = ["january", "february", "march", "april", "may", "june", 
          "july", "august", "september", "october", "november", "december"]

    month = current_time.month
    month = months[month - 1]
    year = current_time.year

    url = f"https://www.ea.com/ja-jp/games/starwars/galaxy-of-heroes/news/{month}-calendar-preview-{year}"


    res = requests.get(url)

    if res.status_code == 200:
        res_text =  res.text

    soup = BeautifulSoup(res_text, "html.parser")

    data = []

    elements = soup.find_all("ea-text")

    for element in elements:
        text = element.text.replace("\xa0", " ")
        lines = text.split("\n")

        for line in lines:
            if line != "":
                if "-" in line:
                    a, b = line.split("-")
                    data.append(a.strip())
                    data.append(b.strip())
                else:
                    data.append(line.strip()) 

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


    currentYear = current_time.year
    currentMonth = current_time.month
    currentDay = current_time.day

    todays_events = []
    for event in events:
        if f"{currentYear}年{currentMonth}月{currentDay}日" in event.get("EventDate"):
            todays_events.append(event)

    return todays_events

output = index()
print(output)