import scrape
#import parse

if __name__ == "__main__":
    cricinfoURL = "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/match-schedule-fixtures-and-results" 
    cricbuzzURL = "https://www.cricbuzz.com/"
    #schedule = scrape.scrapeSchedule(url)
    scrape.scrapeScore(cricbuzzURL)
