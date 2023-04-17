import requests
from bs4 import BeautifulSoup

def scrapeSchedule(url):
    page = requests.get(url)
    print("Type = ", type(page.content))
    soup = BeautifulSoup(page.content, 'html.parser')
    schedule = soup.find_all(attrs= {
                                     'class': 'ds-p-0',   
                                     })
    dates = soup.find_all(attrs= {
                                  'class': 'ds-text-compact-xs ds-font-bold ds-w-24' 
                                  })
    for date in dates:
        print(date.get_text())
    return (schedule)
