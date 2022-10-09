import datetime
import urllib.parse

thumbnails = {
    "codechef.com": "https://i.ibb.co/Jv61LD9/codechef-thumbnail.png",
    "generic": "https://i.ibb.co/xqzqs2m/generic-contest-thumbnail.png",
    "codeforces.com": "https://i.ibb.co/Xzycwsq/codeforces-thumbnail.png"
}

hostList = ["codechef", "codingninjas", "hackerrank"]


def getGoogleCalenderLink(contestDic):
    escpName = urllib.parse.quote(contestDic['name'])
    return f"https://calendar.google.com/calendar/event?action=TEMPLATE&dates={getTimeInGoogleCalFormat(contestDic['start'])}%2F{getTimeInGoogleCalFormat(contestDic['end'])}&text={escpName}&details={contestDic['link']}&location={contestDic['platform']} "


def getTicktickReminderLink(contestDic):
    escpName = urllib.parse.quote(contestDic['name'])
    # ticktick://x-callback-url/v1/add_task?title=buy%20some%20eggs&x-success={{scheme of the next app}}
    return f"ticktick://x-callback-url/v1/add_task?title={escpName}&startDate={getTimeInTickTickFormat(contestDic['start'])}&endDate={contestDic['end']}&priority=3"


def isContestStartingToday(contestStartTime, currentDate):
    return datetime.datetime.fromisoformat(contestStartTime).day == currentDate.day


def getCurrentDatePlus10DaysFormatted():
    return ((datetime.datetime.now() + datetime.timedelta(hours=5, minutes=30)) + datetime.timedelta(
        hours=240)).strftime('%Y-%m-%d')


def getCurrentDate():
    return (datetime.datetime.now() + datetime.timedelta(hours=5, minutes=30)).strftime('%Y-%m-%d')


def getCurrentDateUnFormatted():
    return datetime.datetime.now() + datetime.timedelta(hours=5, minutes=30)


def getCurrentDateTime():
    return datetime.datetime.now()


def getTimeInISO(time):
    istTime = datetime.datetime.fromisoformat(time) + datetime.timedelta(hours=5, minutes=30)
    return istTime.strftime('%d-%b-%y %H:%M:%S %p')


def getTimeInGoogleCalFormat(time):
    return (datetime.datetime.fromisoformat(time)).strftime('%Y%m%dT%H%M%SZ').replace(
        ' ', '')


def getTimeInTickTickFormat(time):
    time = ((datetime.datetime.fromisoformat(time) + datetime.timedelta(hours=5, minutes=30)).strftime(
        '%Y-%m-%dT%H:%M:%S.%f')).replace(
        ' ', '')
    return time[:-3] + '+0530'
