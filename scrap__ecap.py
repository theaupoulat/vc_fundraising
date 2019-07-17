import requests
import tweepy
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import sys

# twitter api identification
"""
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# getting the tweet
ecap = api.get_user("ecappartner")
ecap_text = ecap.status.text
ecap_text = ecap_text.split()

# searching for the link
for i in ecap_text:
    if "https" in i:
        ecap_link = i
        break

"""
# bs content of the newsletter

i = sys.argv[1]
print(i)

result = requests.get(i)
src = result.content

soup = BeautifulSoup(src, 'lxml')
table = soup.find_all("table", class_="mcnCaptionRightTextContentContainer")

# setting up table for date
all = [["week_num", "startup", "amount_raised",
        "sector", "description", "investors"]]

for t in table:
    row = []
    td = t.find("td")

# week_num
    my_date = datetime.date.today()
    week_num = sys.argv[2]  # my_date.isocalendar()[1]
    row.append(week_num)

# name & amount
    h1 = td.h1.text
    h1 = h1.split("- ")
    name = h1[0]
    row.append(name)
    amount = h1[1]
    row.append(amount)

# sector
    sector = td.h2.text
    row.append(sector)

# description
    desc = td.div.text
    row.append(desc)

# investors
    h4 = td.h4.text
    investors = h4[11:].split(', ')
    row.append(investors)

    all.append(row)


# exporting new entries
df = pd.DataFrame(all[1:], columns=all[0])
df.to_csv('levee2019.csv', mode='a', index=False, header=False)
