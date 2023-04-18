import requests
from bs4 import BeautifulSoup

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
    schedule = {}
    for div in panelDiv:
        print(div.get_text())
        print("   ")
        gameDates = div.find_all('div', attrs = {'class': 'ds-text-compact-xs ds-font-bold ds-w-24'})
        matchDetails = div.find_all('div', attrs = {'class': 'ds-flex ds-flex-col ds-mt-2 ds-mb-2'})

        for gameDate in gameDates:
            if len(gameDate) == 0:
                try:
                    currGameDate = prevGameDate
                except Exception as e:
                    raise e
                print("Length = 0")
            else:
                currGameDate = gameDate.get_text()
                prevGameDate = currGameDate
                print("Length != 0")
            gameDateList.append(currGameDate)
            print("gameDate = ", currGameDate)

        for matchDetail in matchDetails:
            print("matchDetail length = ", len(matchDetail))
            print(matchDetail.get_text())
            matchDetailList.append(matchDetail.get_text())

    print("GameDateList = ", gameDateList)
    print("GameDateList Len = ", len(gameDateList))
    print(" ")
    print("Match Detail List = ", matchDetailList)
    print("Match Detail List Len = ", len(matchDetailList))

    for i in range(len(gameDateList)):
        #print(gameDateList.pop(), "--->", matchDetailList.pop())
        schedule[matchDetailList.pop()] = gameDateList.pop()

    for key,value in schedule.items():
        print(key, "--->", value)
    #print("Schedule = ", schedule)

    return panelDiv
