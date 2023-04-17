import scrape

if __name__ == "__main__":
    url = "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/match-schedule-fixtures-and-results" 
    schedule = scrape.scrapeSchedule(url)
    with open('main.txt','w') as file:
        file.write(str(schedule))
    print("DONE WRITING")
