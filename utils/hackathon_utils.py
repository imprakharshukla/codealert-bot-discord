import datetime
from platform import platform
import urllib.parse

thumbnails = {
    "codechef.com": "https://i.ibb.co/Jv61LD9/codechef-thumbnail.png",
    "generic": "https://i.ibb.co/xqzqs2m/generic-contest-thumbnail.png",
    "codeforces.com": "https://i.ibb.co/Xzycwsq/codeforces-thumbnail.png"
}

hostList = ["codechef.com", "codingninjas.com/codestudio"]


def getGoogleCalenderLink(contestDic):
    escpName = urllib.parse.quote(contestDic['name'])
    platformName = urllib.parse.quote(contestDic['platform'])
    return f"https://calendar.google.com/calendar/event?action=TEMPLATE&dates={getTimeInGoogleCalFormat(contestDic['start'])}%2F{getTimeInGoogleCalFormat(contestDic['end'])}&text={escpName}&details={contestDic['link']}&location={platformName} "


def getTicktickReminderLink(contestDic):
    escpName = urllib.parse.quote(contestDic['name'])
    # ticktick://x-callback-url/v1/add_task?title=buy%20some%20eggs&x-success={{scheme of the next app}}
    return f"ticktick://x-callback-url/v1/add_task?title={escpName}&startDate={getTimeInTickTickFormat(contestDic['start'])}&endDate={contestDic['end']}&priority=3"


def getCurrentDate():
    return datetime.datetime.now().strftime('%Y-%m-%d')


def getTimeInISO(time):
    istTime = datetime.datetime.fromisoformat(
        time) + datetime.timedelta(hours=5, minutes=30)
    return istTime.strftime('%d-%b-%y %H:%M:%S %p')

def daysLeft(startDate):
    start = datetime.datetime.fromisoformat(startDate).strftime('%d-%b-%y %H:%M:%S %p')
    now = datetime.datetime.now().strftime('%d-%b-%y %H:%M:%S %p')
    start = datetime.datetime.strptime(start, '%d-%b-%y %H:%M:%S %p')
    now = datetime.datetime.strptime(now, '%d-%b-%y %H:%M:%S %p')
    return str((start - now).days)

    

def getTimeInGoogleCalFormat(time):
    return (datetime.datetime.fromisoformat(time)).strftime('%Y%m%dT%H%M%SZ').replace(' ','')


def getTimeInTickTickFormat(time):
    time = ((datetime.datetime.fromisoformat(time) + datetime.timedelta(hours=5, minutes=30)).strftime(
        '%Y-%m-%dT%H:%M:%S.%f')).replace(
        ' ', '')
    return time[:-3] + '+0530'
