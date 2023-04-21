import requests
from bs4 import BeautifulSoup
from collections import defaultdict

def scrapeSchedule(url):
    page = requests.get(url)
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

    return schedule

def getLiveScore(url):
    page = requests.get(url)
    print(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    liveScoreCard = soup.find_all('div', attrs={'class': 'cb-col-67 cb-col'})
    print(liveScoreCard)

    return liveScoreCard

def scrapeScore(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    matches = soup.find_all('li', attrs={'class': 'cb-view-all-ga cb-match-card cb-bg-white'})
    iplMatches = []
    iplMatchesSrc = []
    
    for match in matches:
        matchInfo = match.get_text()
        if "Indian Premier League 2023" in matchInfo:
            matchClass = match.find('div', attrs={'class': 'cb-font-12'})['class']
            #print(matchClass)
            if "cb-text-complete" in matchClass:
                iplMatchesSrc.append(match)
                iplMatches.append(matchInfo)
                print("Match Over")
            elif "cb-text-preview" in matchClass:
                print("Match yet to begin")
            elif "cb-text-in-progress" in matchClass:
                print("Toss Over - Match yet to begin")
            elif "cb-text-live" in matchClass:
                print("Live Match Happening")
                iplMatchesSrc.append(match)
                iplMatches.append(matchInfo)
    # scorecard div-class cb-col-67 cb-col   
    #print(iplMatches)
    #After getting all the IPL matches go to the live match link
    numIplMatches = len(iplMatches)
    for i in range(numIplMatches):
        linkToMatch = url + iplMatchesSrc[i].find('a')['href']     
        getLiveScore(linkToMatch)

    return iplMatches
