import requests
from bs4 import BeautifulSoup
from collections import defaultdict

def scrapeSchedule(url):
    page = requests.get(url)
    print("Type = ", type(page.content))
    soup = BeautifulSoup(page.content, 'html.parser')
    panelDiv = soup.find_all(attrs= {
                                     'class': 'ds-p-4'   
                                     })
    numSpaces = 20
    print("Date", numSpaces*" ", "Match Details", numSpaces*" ", "Time")
    matchDetailList = []
    gameDateList = []
    schedule = defaultdict(list)

    for div in panelDiv:
        gameDates = div.find_all('div', attrs = {'class': 'ds-text-compact-xs ds-font-bold ds-w-24'})
        matchDetails = div.find_all('div', attrs = {'class': 'ds-flex ds-flex-col ds-mt-2 ds-mb-2'})

        for gameDate in gameDates:
            if len(gameDate) == 0:
                try:
                    currGameDate = prevGameDate
                except Exception as e:
                    raise e
            else:
                currGameDate = gameDate.get_text()
                prevGameDate = currGameDate
            gameDateList.append(currGameDate)

        for matchDetail in matchDetails:
            matchDetailList.append(matchDetail.get_text())

    for i in range(len(gameDateList)):
        schedule[gameDateList.pop()].append(matchDetailList.pop())

    #for key,value in schedule.items():
    #    print(key, "--->", value)

    return schedule
