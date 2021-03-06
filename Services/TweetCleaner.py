import re
import xml.etree.ElementTree
import emoji
from unidecode import unidecode


class TweetCleaner(object):

    def removeTags(self, text):

        try:
            text = ''.join(xml.etree.ElementTree.fromstring("<p>" + text + "</p>").itertext())
        finally:
            return text

    def processTweet(self, tweetraw):
        tweet = emoji.demojize(tweetraw, delimiters=(" :", ": "))

        # To unicode
        tweet = unidecode(tweet)

        # Convert to lower case
        tweet = tweet.lower()
        # Convert www.* or https?://* to URL
        tweet = re.sub('((www\.[^\s]+)|(https?:/[^\s]+))', '', tweet)
        # Removing \n
        tweet = tweet.replace('\n', ' ')
        # Convert @username to AT_USER
        tweet = re.sub('@[^\s]+', 'AT_USER', tweet)
        # Remove additional white spaces
        tweet = re.sub('[\s]+', ' ', tweet)
        # Replace #word with word
        tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
        # Trim
        tweet = tweet.strip()

        #Removing HTML tags
        tweet = self.removeTags(tweet)

        # Replacing unknown chars
        tweet = tweet.replace('[?]', '')
        tweet = tweet.replace('&amp;', '&')
        tweet = tweet.replace('&lt;', '<')
        tweet = tweet.replace('&gt;', '>')

        # encontrar uma lib que possa fazer essa substituição

        return tweet
