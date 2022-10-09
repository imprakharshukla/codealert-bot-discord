import requests
import os
import json
import datetime

from dotenv import load_dotenv

from discordHelper import hackathon_discord
from discordHelper.hackathon_discord import sendNoContestsToday
from settings import ENV

from utils import hackathon_utils
from utils.hackathon_utils import formatPrize, getTimeInISO, getGoogleCalenderLink, formatPrize

if ENV == "DEV":
    load_dotenv()


def fetchHackathonAPI():
    URL = "https://unstop.com/api/public/opportunity/search-new?opportunity=hackathons&sort=daysleft&dir=asc&filters=All,All,open,3&types=payment,eligible,oppstatus,teamsize&atype=explore&page=1&showOlderResultForSearch=true"

    response = requests.get(URL)
    hackathonData = response.json()['data']['data']

    hackathons = []

    for hack in hackathonData:
        startDate = getTimeInISO(hack['start_date'])
        daysLeft = hackathon_utils.daysLeft(hack['start_date'])

        if (int(daysLeft) > 0):
            hackObj = {}
            hackObj['id'] = hack['id']
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
            if (hack['isPaid']):
                hackObj['isPaid'] = True
                hackObj['prize'] = formatPrize(hack['prizes'][0])
            else:
                hackObj['isPaid'] = False
                hackObj['prize'] = "No Prize"
            hackathons.append(hackObj)
    if (len(hackathons) == 0):
        sendNoContestsToday()
    else:
        hackathon_discord.sendContestAlerts(hackathons)