import requests
from dotenv import load_dotenv

from discordHelper import hackathon_discord
from discordHelper.hackathon_discord import sendNoContestsToday
from settings import ENV
from utils import hackathon_utils
from utils.hackathon_utils import getTimeInISO, getGoogleCalenderLink, formatPrize

if ENV == "DEV":
    load_dotenv()

import datetime
from dateutil import tz
import urllib.parse

def getDateFromISO(time):
    istTime = datetime.datetime.fromisoformat(time)
    return istTime.strftime('%d-%b-%y')


def getGoogleCalenderLink(contestDic):
    escpName = urllib.parse.quote(str(contestDic["name"])or"")
    platformName = urllib.parse.quote(str(contestDic["platform"])or"")
    return f"https://calendar.google.com/calendar/event?action=TEMPLATE&dates={getTimeInGoogleCalFormat(contestDic['start'])}%2F{getTimeInGoogleCalFormat(contestDic['end'])}&text={escpName}&details={contestDic['link']}&location={platformName} "


def getTimeInGoogleCalFormat(time):
    return (datetime.datetime.fromisoformat(time)).strftime('%Y%m%dT%H%M%SZ').replace(' ', '')


def fetchDevfolioHackathonAPI():

    url = "https://api.devfolio.co/api/search/hackathons"


    payload = {
        "type": "application_open",
        "from": 0,
        "size": 100
    }
    headers = {"Content-Type": "application/json"}

    response = requests.request("POST", url, json=payload, headers=headers)

    hackathons = response.json()['hits']['hits']

    formatedHackathonsData=[]
    for hack in hackathons:
        startDate = hack['_source']['hackathon_setting']['reg_ends_at']
        
        from_zone = tz.gettz('UTC')
        to_zone = tz.gettz('Asia/Kolkata')
        utc = datetime.datetime.strptime(startDate, '%Y-%m-%dT%H:%M:%S%z')
        utc = utc.replace(tzinfo=from_zone)
        ist = utc.astimezone(to_zone)        
        #find days left without using hackathon_utils
        now = datetime.datetime.now()
        now = now.replace(tzinfo=to_zone)
        secondsLeft = (ist - now).seconds  
        daysLeft = (ist - now).days      


        if int(secondsLeft) > 0:
            # print(hack['_source']['uuid'])
            # print(hack['_source']['name'])
            # print(hack['_source']['starts_at'])
            # print('https://'+hack['_source']['slug']+'.devfolio.co')
            # print(hack['_source']['ends_at'])
            # print(hack['_source']['hackathon_setting']['reg_starts_at'])
            # print(hack['_source']['hackathon_setting']['reg_ends_at'])
            # print(hack['_source']['hackathon_setting']['women_only'])
            # print(hack['_source']['cover_img'])
            # print(hack['_source']['is_online'])
            # print('-------------------------------------------')
            hackObj = {}
            hackObj['id'] = hack['_source']['uuid']
            hackObj['name'] = hack['_source']['name']
            hackObj['start_iso'] = getDateFromISO(hack['_source']['starts_at'])
            hackObj['end_iso'] = getDateFromISO(hack['_source']['ends_at'])
            hackObj['start'] = hack['_source']['starts_at']
            hackObj['end'] = hack['_source']['ends_at']
            hackObj['link'] = 'https://'+hack['_source']['slug']+'.devfolio.co'
            hackObj['thumbnail'] = hack['_source']['cover_img']
            hackObj['platform'] = hack['_source']['location']
            hackObj['regEnd'] = daysLeft
            hackObj['calender_event'] = getGoogleCalenderLink(hackObj)        
            hackObj['isPaid'] = False
            if (hack['_source']['is_online']):
                hackObj['prize'] = "Online"
            else:
                hackObj['prize'] = "Offline"
            formatedHackathonsData.append(hackObj)

    return formatedHackathonsData

res = fetchDevfolioHackathonAPI()
hackathon_discord.sendContestAlerts(res)


    # # for hack in hackathonData:
    # #     startDate = getTimeInISO(hack['start_date'])
    # #     daysLeft = hackathon_utils.daysLeft(hack['start_date'])

    # #     if int(daysLeft) > 0:
    # #         hackObj = {}
    # #         hackObj['id'] = hack['id']
    # #         hackObj['name'] = hack['title']
    # #         hackObj['start'] = hack['start_date']
    # #         hackObj['end'] = hack['end_date']
    # #         hackObj['start_iso'] = startDate
    # #         hackObj['end_iso'] = getTimeInISO(hack['end_date'])
    # #         hackObj['link'] = hack['seo_url']
    # #         hackObj['thumbnail'] = hack['banner_mobile']['image_url']
    # #         hackObj['platform'] = hack['organisation']['name']
    # #         hackObj['regEnd'] = hack['regnRequirements']['remain_days']
    # #         hackObj['calender_event'] = getGoogleCalenderLink(hackObj)
    # #         if hack['isPaid']:
    # #             hackObj['isPaid'] = True
    # #             hackObj['prize'] = formatPrize(hack['prizes'][0])
    # #         else:
    # #             hackObj['isPaid'] = False
    # #             hackObj['prize'] = "No Prize"
    # #         hackathons.append(hackObj)

    # # # Fetching Hackathon from devpost.com
    


