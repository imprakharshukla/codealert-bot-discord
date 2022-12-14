import datetime
import os

import requests
from dotenv import load_dotenv

from discordHelper import webhook_manager
from discordHelper.webhook_manager import sendNoContestsToday
from settings import ENV
from utils import contest_utils
from utils.contest_utils import getTimeInISO, getGoogleCalenderLink, getTicktickReminderLink, getCurrentDate, \
    isContestStartingToday, getCurrentDatePlus10DaysFormatted, hostList

if ENV == "DEV":
    load_dotenv()


def fetchContestAPI():
    contestDic = {}
    contestList = []
    currentDate = getCurrentDate()
    print(getCurrentDatePlus10DaysFormatted())
    response = requests.get(
        f"{os.environ.get('BASE_URL')}/?username={os.environ.get('USERNAME')}&api_key={os.environ.get('TOKEN')}&start__gte={currentDate}T00:30:00&end__lte={getCurrentDatePlus10DaysFormatted()}T18:29:00")
    # response = requests.get(
    #     f"{os.environ.get('BASE_URL')}/?username={os.environ.get('USERNAME')}&api_key={os.environ.get('TOKEN')}&start__gte=2022-10-07T00:30:00&end__lte={getCurrentDatePlus10DaysFormatted()}T18:29:00")

    contestData = response.json()['objects']
    if len(contestData) == 0:
        sendNoContestsToday()
    else:
        for contest in contestData:
            if isContestStartingToday(contest["start"], datetime.datetime.fromisoformat(currentDate)):

                # Checking if the contest is important
                isImportant = [con for con in hostList if (con in contest["host"])]
                contestDic["isImp"] = bool(isImportant)
                contestDic["name"] = contest["event"]
                contestDic["platform"] = contest["host"]
                contestDic["link"] = contest["href"]
                contestDic["start_iso"] = getTimeInISO(contest["start"])
                contestDic["end_iso"] = getTimeInISO(contest["end"])
                contestDic["start"] = (contest["start"])
                contestDic["end"] = (contest["end"])
                contestDic["calender_event"] = getGoogleCalenderLink(contestDic)
                contestDic["ticktick_task"] = getTicktickReminderLink(contestDic)
                if contest["host"] in contest_utils.thumbnails:
                    contestDic["thumbnail"] = contest_utils.thumbnails[contest["host"]]
                else:
                    contestDic["thumbnail"] = contest_utils.thumbnails["generic"]

                tempDic = contestDic.copy()
                contestList.append(tempDic)
                contestDic.clear()

    webhook_manager.sendContestAlerts(contestList, )
