import requests
import os
import json
import datetime

from dotenv import load_dotenv

from discordHelper import webhook_manager
from discordHelper.webhook_manager import sendNoContestsToday
from settings import ENV

from utils import hackathon_utils
from utils.hackathon_utils import getTimeInISO, getGoogleCalenderLink, getTicktickReminderLink, getCurrentDate

if ENV == "DEV":
    load_dotenv()


def fetchHackathonAPI():
    URL = "https://unstop.com/api/public/opportunity/search-new?opportunity=hackathons&sort=daysleft&dir=asc&filters=All,All,open,3&types=payment,eligible,oppstatus,teamsize&atype=explore&page=1&showOlderResultForSearch=true"

    response = requests.get(URL)
    hackathonData = response.json()['data']['data']

    # save hackathonData array to a json file
    with open('./hackathonData.json', 'w') as outfile:
        json.dump(hackathonData[0], outfile)

    for hack in hackathonData:
        hackObj = {}
        startDate = getTimeInISO(hack['start_date'])
        # find days left from start date and current date
        daysLeft = hackathon_utils.daysLeft(hack['start_date'])
        if (int(daysLeft) > 0):
            hackObj['name'] = hack['title']
            hackObj['start'] = hack['start_date']
            hackObj['end'] = hack['end_date']
            hackObj['start_iso'] = startDate
            hackObj['end_iso'] = getTimeInISO(hack['end_date'])
            hackObj['link'] = hack['seo_url']
            hackObj['thumbnail'] = hack['banner_mobile']['image_url']
            hackObj['platform'] = hack['organisation']['name']
            hackObj['regEnd'] = hack['regnRequirements']['remain_days']
            hackObj['calender_event'] = getGoogleCalenderLink(hackObj)
            print("Name: " + hack['title'])
            print("Start Date: " + startDate)
            print("Days Left: " + daysLeft)
            print("Link: " + hack['seo_url'])
            print("Thumbnail: " + hack['banner_mobile']['image_url'])
            print("Platform: " + hack['organisation']['name'])
            print("Reg End: " + hack['regnRequirements']['remain_days'])
            print("Calender Event: " + getGoogleCalenderLink(hackObj))
            if (hack['isPaid']):
                print("prize: " + str(hack['prizes'][0]['cash']
                                      ) + " " + hack['prizes'][0]['currency'])
            print("--------------------------------------------------")
