import twitter
import csv
import json
import urllib
import peewee
from peewee import *

def createQuery(file):
    query = 'q='
    first_line = file.readline().replace('#', '%23').strip('\n')
    query += first_line
    for hashtag in file:
        query += '%2C%20OR%20' + hashtag.replace('#', '%23').strip('\n')
    query += '&src=typd&count=100'
    return query


def getTweets(query, party):
    results = api.GetSearch(raw_query=query)
    for result in results:
        if result.place is not None:
            bounding_box = result.place.get('bounding_box').get('coordinates')[0]
            tweet = Tweet((bounding_box[0][0] + bounding_box[1][0]) / 2, (bounding_box[1][1] + bounding_box[2][1]) / 2,
                          party, result.created_at)
            tweets.append(tweet)
        if (result.user.geo_enabled is True) and (len(result.user.location) > 0):
            locationsent = 0
            for state in mydict:
                test1 = state[0] + ","
                test2 = state[0] + " "
                if test1.lower() in result.user.location.lower() or test2.lower() in result.user.location.lower() or state[2].lower() in result.user.location.lower():
                    stateid = state[0]
                    for city in mydict2[stateid]:
                        if city[0].lower() in result.user.location.lower():
                            response = urllib.request.urlopen("http://api.zippopotam.us/us/" + city[1]).read().decode('utf-8')
                            data = json.loads(response)
                            if data.get('places')[0].get('latitude') == None or data.get('places')[0].get('longitude') == None:
                                break
                            tweet = Tweet(data.get('places')[0].get('latitude'), data.get('places')[0].get('longitude'), party,result.created_at)
                            tweets.append(tweet)
                            locationsent = 1
                            break
                    if locationsent == 0:
                        for state in mydict:
                            if state[0] == stateid:
                                response = urllib.request.urlopen("http://api.zippopotam.us/us/" + state[1]).read().decode('utf-8')
                                data = json.loads(response)
                                if data.get('places')[0].get('latitude') == None or data.get('places')[0].get('longitude') == None:
                                    break
                                tweet = Tweet(data.get('places')[0].get('latitude'), data.get('places')[0].get('longitude'), party, result.created_at)
                                tweets.append(tweet)
                                locationsent = 1
                                break

                if locationsent == 0:
                    if result.user.location.lower() == "usa" or result.user.location.lower() == "us" or result.user.location.lower() == "united states" or result.user.location.lower() == "united states of america" :
                        tweet = Tweet(34.024212, -118.496475, party, result.created_at)
                        tweets.append(tweet)
                        locationsent = 1

                if locationsent == 1:
                    break


class Tweet:
    def __init__(self, latitude, longitude, party, timestamp):
        self.latitude = latitude
        self.longitude = longitude
        self.party = party
        self.timestamp = timestamp

api = twitter.Api(consumer_key='rnBTENQ1GCJdZLVEuZheV6YJ6',
                  consumer_secret='b9g5TgNIXRKN7lwQxh5YcLk8AI59zQK3zzIAtAorspMHpUha3F',
                  access_token_key='787504691949076481-jwZbK3F3lc5evdzeExZO0DRj4LvWB1m',
                  access_token_secret='Q8DGppRwEFKWo5ZxbAjXCQUGAqBgCMU0t4ZI21RGoND3T')

db = MySQLDatabase('politicsdb', host='politicsdb.cdcme9z9rkbx.us-west-2.rds.amazonaws.com',
                   port=3306, user='richardding')
db.connect()

republican_file = open('../data/republican_hashtags.txt', 'r')
democrat_file = open('../data/democrat_hashtags.txt', 'r')
# q=%23Trump%2C%20OR%20%23Hillary%2C%20OR%20%23Kane&count=100
republican_query = createQuery(republican_file)
democrat_query = createQuery(democrat_file)

with open('../data/StateZip.csv', mode='r') as infile:
    reader = csv.reader(infile)
    mydict = [[rows[0], rows[1], rows[2]] for rows in reader]



mydict2 = {}
for state in mydict:
    currentlist = []
    with open('../data/Zipcodes.csv', mode='r') as infile:
        reader = csv.reader(infile)
        for row in reader:
            if row[4] == state[0]:
                currentlist.append([row[3],row[1]])
        mydict2[state[0]] = currentlist

tweets = []
for i in range(0, 20):
    getTweets(republican_query, 'Republican')
    getTweets(democrat_query, 'Democrat')
print(tweets)

for tweet in tweets:
    print(tweet)

