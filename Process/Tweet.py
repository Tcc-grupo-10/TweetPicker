class Tweet(object):

    def __init__(self, raw_tweet):
        self.rawTweet = raw_tweet
        self.preprocessedTweet = None
        self.sentiment = None
        self.isSpam = False
