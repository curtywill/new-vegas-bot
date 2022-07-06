'''

Author: Curtiss Williams
Description: Scrapes character dialouge from the Fallout Wiki, then
populates a Firebase database with the data as well as
saving .json files locally with the data.

'''
from bs4 import BeautifulSoup
import requests
import re
import json
import firebase_admin
from firebase_admin import db
from firebase_admin import credentials

URL = "https://fallout.fandom.com/api.php"

def get_dialouge(page):
    params = {
        'action': 'parse',
        'format': 'json',
        'formatversion': '2',
        'page': page,
        'prop': 'text'
    }

    r = requests.get(URL, params=params)
    va_table_html = r.json()["parse"]["text"]
    soup = BeautifulSoup(va_table_html, "lxml")
    quotes = []
    for table in soup.find_all("table", class_="va-table va-table-full np-table-dialogue"):
        for tr in table.find_all("tr"):
            row = tr.find_all("td")
            if len(row) == 0:
                continue
            quote = re.sub("\s?\{.*?\}\s?"," ",row[len(row)-2].text).strip()
            if len(quote) > 0:
                quotes.append(quote)
    return quotes

def get_titles():
    params = {
        'action': 'query',
        'format': 'json',
        'formatversion': '2',
        'list': 'categorymembers',
        'cmtitle': 'Category:Fallout:_New_Vegas_dialogue_files',
        'cmlimit':'500'
    }
    r = requests.get(url=URL,params=params).json()
    cont = r["continue"]["cmcontinue"]
    titles = [title["title"] for title in r["query"]["categorymembers"]]
    params['cmlimit'] = '11'
    params['cmcontinue'] = cont
    r = requests.get(url=URL,params=params).json()
    titles1 = [title["title"] for title in r["query"]["categorymembers"]]
    titles.extend(titles1)

    return titles

def main():
    cred = credentials.Certificate("service-file.json")
    firebase_admin.initialize_app(cred, {"databaseURL":"databaseURL"})
    ref = db.reference("/")
    ref.set({})
    titles = get_titles()
    for title in titles:
        lines = get_dialouge(title)
        with open(title[0:-4]+".json", "w") as outfile:
            json.dump({title[0:-4]: lines}, outfile)
        ref.push().set(lines)
    print("all done")

if __name__ == '__main__':
    main()
