import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import notifyme

# Series
ipl_2023 = "Indian Premier League 2023"
# Match State strs
matchState = {
                "Over": "cb-text-complete",
                "In Progress": "cb-text-in-progress",
                "Yet to Start": "cb-text-preview",
                "Live": "" # Check this when match is live
             }

# Header Strs
batterStr = "Batter"
bowlerStr = "Bowler"
erStr = "ECO"
srStr = "SR"

def scrapeSchedule(url):
    """
    Scrapes Game Schedule from cricinfo
    Params: (IN)  url to cricinfo
            (OUT) schedule as a dictionary
    """

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
    """
    Gets Live Score if a live game is Happening
    Params: (IN)  url
            (OUT) live sore card
    """
    
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    playersDiv = soup.find_all('div', attrs={'class': 'cb-min-inf cb-col-100'})

    # Get Bowler info
    bowlerInfo = ""
    batterInfo = ""
    populatingBatterHeader = False
    populatingBowlerHeader = False
    populatedBatter = False
    populatedBowler = False
    populatedBatterHeader = False
    populatedBowlerHeader = False
    batterHeaderInfo = ""
    bowlerHeaderInfo = ""
    for playersInfo in playersDiv:
        for players in playersInfo:
            for player in players:
                parsedText = player.get_text()
                if (parsedText == batterStr):
                    populatingBatterHeader = True
                    batterHeaderInfo += parsedText + "                    "
                elif (parsedText == srStr):
                    batterHeaderInfo += parsedText
                    populatedBatterHeader = True
                    populatingBatterHeader = False
                elif (parsedText == bowlerStr):
                    populatedBatter = True
                    populatingBowlerHeader = True
                    bowlerHeaderInfo += parsedText + "                    "
                elif (parsedText == erStr):
                    bowlerHeaderInfo += parsedText
                    populatedBowlerHeader = True
                    populatingBowlerHeader = False
                else:
                    if (populatingBatterHeader == True):
                        batterHeaderInfo += parsedText + "      "
                    elif (populatingBowlerHeader == True):
                        bowlerHeaderInfo += parsedText + "      "
                    elif (populatedBatterHeader == True) and (populatedBatter == False):
                        batterInfo += parsedText + "    "
                    elif (populatedBowlerHeader == True) and (populatedBowler == False):
                        bowlerInfo += parsedText + "    "
            if (len(batterInfo) > 1) and (populatedBatter == False):
                batterInfo += "\n"
            if (len(bowlerInfo) > 1):
                bowlerInfo += "\n"

    scoreBoard = soup.find_all('div', attrs={'class': 'cb-col cb-col-67 cb-scrs-wrp'})
    teamScore = ""
    for scores in scoreBoard:
        for score in scores:
            teamScore += score.get_text()
            teamScore += "\n"

    scoreCard = teamScore + batterHeaderInfo + "\n" + batterInfo + "\n" + bowlerHeaderInfo + "\n" + bowlerInfo
    return scoreCard

def getScore(url):
    """
    Checks calls getLiveScore() if the game is Live, if not calls getStartTime()
    to get next live match info
    Params: (IN)  url
            (OUT) live scoreCard
    """
    
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    matches = soup.find_all('li', attrs={'class': 'cb-view-all-ga cb-match-card cb-bg-white'})
    iplMatches = []
    iplMatchesSrc = []
    nextMatchesSrc = []
    nextMatches = []

    for match in matches:
        matchInfo = match.get_text()
        if ipl_2023 in matchInfo:
            matchClass = match.find('div', attrs={'class': 'cb-font-12'})['class']
            if matchState["Over"] in matchClass:
                continue
            elif matchState["Yet to Start"] in matchClass:
                nextMatchesSrc.append(match)
                nextMatches.append(matchInfo)
            elif matchState["In Progress"] in matchClass:
                continue
            else:
                print("Live Match Happening")
                iplMatchesSrc.append(match)
                iplMatches.append(matchInfo)

    #After getting all the IPL matches go to the live match link
    numIplMatches = len(iplMatches)
    numUpcomingMatches = len(nextMatches)
    scoreCard = ""
    if (numIplMatches == 0):
        for i in range(numUpcomingMatches):
            linkToNextMatch = url + nextMatchesSrc[i].find('a')['href']
            startTime = getStartTime(linkToNextMatch)
            print("No Live Matches now. Next Match on", startTime)
    else:
        for i in range(numIplMatches):
            linkToMatch = url + iplMatchesSrc[i].find('a')['href']
            print(linkToMatch)
            scoreCard = getLiveScore(linkToMatch)
            print(scoreCard)
        notifyme.notifyMe(scoreCard)

    return scoreCard

def getStartTime(url):
    """
    Get Start Time of the match
    Params: (IN)  url
            (OUT) start time
    """

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    startingIn = soup.find_all('span', attrs={'itemprop': 'startDate'})
    time = ""
    for startTime in startingIn:
        time = startTime.get_text()
    if "LOCAL" in time:
        time = time.replace('LOCAL', 'IST')

    return time
