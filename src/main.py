import scrape
import time

if __name__ == "__main__":
    cricinfoURL = "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/match-schedule-fixtures-and-results" 
    cricbuzzURL = "https://www.cricbuzz.com/"
    scoreCard = scrape.getScore(cricbuzzURL)
    scoreCardLen = len(scoreCard)
    
    # Keep notifying while there is a live match
    # TBD Later - Instead of notifying every 2 mins - notify if a wicket falls
    while (scoreCardLen != 0):
        time.sleep(120)
        scoreCard = scrape.getScore(cricbuzzURL)
        print(scoreCard)
        scoreCardLen = len(scoreCard)
