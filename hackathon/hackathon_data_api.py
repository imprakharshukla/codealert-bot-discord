import requests
from dotenv import load_dotenv

from discordHelper import hackathon_discord
from discordHelper.hackathon_discord import sendNoContestsToday
from settings import ENV
from utils import hackathon_utils
from utils.hackathon_utils import getTimeInISO, getGoogleCalenderLink, formatPrize

if ENV == "DEV":
    load_dotenv()


def fetchHackathonAPI():
    hackathons = []


    # Fetching Hackathon from UNSTOP

    URL = "https://unstop.com/api/public/opportunity/search-new?opportunity=hackathons&sort=daysleft&dir=asc&filterxs=All,All,open,3&types=payment,eligible,oppstatus,teamsize&atype=explore&page=1&showOlderResultForSearch=true "

    response = requests.get(URL)
    hackathonData = response.json()['data']['data']

    for hack in hackathonData:
        startDate = getTimeInISO(hack['start_date'])
        daysLeft = hackathon_utils.daysLeft(hack['start_date'])

        if int(daysLeft) > 0:
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
            if hack['isPaid']:
                hackObj['isPaid'] = True
                hackObj['prize'] = formatPrize(hack['prizes'][0])
            else:
                hackObj['isPaid'] = False
                hackObj['prize'] = "No Prize"
            hackathons.append(hackObj)

    # Fetching Hackathon from devpost.com
    



    hackathon_discord.sendContestAlerts(hackathons)