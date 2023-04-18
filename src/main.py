import scrape

if __name__ == "__main__":
    url = "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/match-schedule-fixtures-and-results" 
    schedule = scrape.scrapeSchedule(url)
    print(schedule)
