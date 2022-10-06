import requests

URL = "https://unstop.com/api/public/opportunity/search-new?opportunity=hackathons&sort=daysleft&dir=asc&filters=All,All,open,3&types=payment,eligible,oppstatus,teamsize&atype=explore&page=1&showOlderResultForSearch=true"

response = requests.get(URL)
hackathonData = response.json()['data']['data']
hackathons = []
for hackathon in hackathonData:
    hackathons.append(hackathon)

for hack in hackathons:
    print(hack)
