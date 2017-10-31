import urllib
import urllib.request
import json
from Services import TwitterIntegration, TweetCleaner
from urllib.request import Request, urlopen
import xlrd
import csv
import time

class TweetFinder:
    def __init__(self, id, label):
        self.id = id
        self.label = label
        self.text = []


def findTweets(id,bearerToken):
    url = 'https://api.twitter.com/1.1/statuses/lookup.json?id=' + id
    req = urllib.request.Request(url)
    req.add_header('Authorization', bearerToken)
    response = urlopen(req).read()
    jsonO = json.loads(response)
    return jsonO


def run():
    tokenUserless = TwitterIntegration.getTokenUserless()
    workbook = xlrd.open_workbook("C:\\Users\\EricContreraCampanat\\Documents\\TCC\\journal.pone.0182487.s003.xlsx")
    sheets = workbook.sheet_names()
    tweetList = []
    for sheet_name in sheets:
        sh = workbook.sheet_by_name(sheet_name)
        for rownum in range(sh.nrows):
            row_valaues = sh.row_values(rownum)
            tweetList.append((row_valaues[0], int(row_valaues[1])))
    # Todas as strings da Lista de strings tweetList serão instanciadas na lista de objetos allTweets
    allTweets = [TweetFinder(tweetId,label) for (tweetId,label) in tweetList]

    fi = open("C:\\Users\\EricContreraCampanat\\Documents\\TCC\\test.csv", "w", newline='')
    f = csv.writer(fi)
    f.writerow(["tweet_id", " label", " text"])
    fi.flush()
    tweetApiList = [allTweets[i:i+100] for i in range(0, len(allTweets), 100)]
    for tweets in tweetApiList:
        #try:
        tweet = []
        for x in tweets:
            tweet.append(x.id)
            # twitter.com/anyuser/status/
        tweet = ",".join(tweet)
        jsonO = findTweets(tweet, tokenUserless)
        jsonStr = []
        for jIndex, json in enumerate(jsonO):
            jsonStr.append(json['id'])

            tweet = list(filter(lambda x: x.id == json['id_str'], tweets))
            if(len(tweet) == 1):
                tweet[0].text = TweetCleaner.processTweet(json['text'])
                print(json['id'])

            """for tweet in tweets:
                if json['id_str'] == tweet.id:
                    tweet.text = json['text'].encode('utf-8')
                    print(json['id'])"""


            f.writerow([tweet[0].id, " {}".format(tweet[0].label), " {}".format(tweet[0].text)])
            fi.flush()
    """except:
            print(time.localtime())
            time.sleep(60 * 15)
            continue"""

    fi.close()
    print("======================================================")






        # twitter.com/anyuser/status/


run()