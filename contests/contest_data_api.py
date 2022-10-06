import os

import requests
from dotenv import load_dotenv

from discordHelper import webhook_manager
from utils import contest_utils
from utils.contest_utils import getTimeInISO, getGoogleCalenderLink

load_dotenv()

contest = []

contestDic = {}
contestList = []

response = requests.get(
    f"{os.environ.get('BASE_URL')}/?username={os.environ.get('USERNAME')}&api_key={os.environ.get('TOKEN')}&start__gte=2022-10-10T12:30:00&end__lt=2022-10-10T18:29:00")

contestData = response.json()['objects']
for contest in contestData:
    contestDic["name"] = contest["event"]
    contestDic["platform"] = contest["host"]
    contestDic["link"] = contest["href"]
    contestDic["start_iso"] = getTimeInISO(contest["start"])
    contestDic["end_iso"] = getTimeInISO(contest["end"])
    contestDic["start"] = (contest["start"])
    contestDic["end"] = (contest["end"])
    contestDic["calender_event"] = getGoogleCalenderLink(contestDic)
    if contest["host"] in contest_utils.thumbnails:
        contestDic["thumbnail"] = contest_utils.thumbnails[contest["host"]]
    else:
        contestDic["thumbnail"] = contest_utils.thumbnails["generic"]
    tempDic = contestDic.copy()
    contestList.append(tempDic)
    contestDic.clear()

webhook_manager.sendContestAlerts(contestList)
