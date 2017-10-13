import Database
import DatabaseCreator
import re
from unidecode import unidecode
import emoji
import xml.etree.ElementTree


def removeTags(text):

    try:
        text = ''.join(xml.etree.ElementTree.fromstring("<p>" + text + "</p>").itertext())
    finally:
        return text


def processTweet(tweet):
    tweet = emoji.demojize(tweet, delimiters=(" :", ": "))

    # To unicode
    tweet = unidecode(tweet)
    tweet = unicode(tweet)

    # Convert to lower case
    tweet = tweet.lower()
    # Convert www.* or https?://* to URL
    tweet = re.sub('((www\.[^\s]+)|(https?:/[^\s]+))', '', tweet)
    # Removing \n
    tweet = tweet.replace('\n', ' ')
    # Remove additional white spaces
    tweet = re.sub('[\s]+', ' ', tweet)
    # Replace #word with word
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    # Trim
    tweet = tweet.strip()

    #Removing HTML tags
    tweet = removeTags(tweet)

    # Replacing unknown chars
    tweet = tweet.replace('[?]', '')
    tweet = tweet.replace('&amp;', '&')
    tweet = tweet.replace('&lt;', '<')
    tweet = tweet.replace('&gt;', '>')

    # encontrar uma lib que possa fazer essa substituição

    return tweet


# Script \/

# Get the service resource.
dynamodb = Database.dynamodb
tweetRTTable = DatabaseCreator.tweetRTTable(dynamodb)
unTweeterizeTable = DatabaseCreator.unTweeterizeTable(dynamodb)

response = tweetRTTable.scan()
allTweets = response['Items']
print len(allTweets)

while 'LastEvaluatedKey' in response:
    response = tweetRTTable.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
    allTweets.extend(response['Items'])
    print len(allTweets)

for tweet in allTweets:
    tweet["text"] = processTweet(tweet["text"])
    print tweet["text"]
    Database.insertItem(tweet, unTweeterizeTable)
