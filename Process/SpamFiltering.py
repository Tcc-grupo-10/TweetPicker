# from Databases import Database
from Services.SpamSet import SpamSet

class SpamFiltering(object):

    def __init__(self):
        self.spamSet = SpamSet()

    def setAsSpam(self, tweet):
        """Database.rawTweets.update_item(
            Key={'tweet_id': tweet_id},
            UpdateExpression="set is_spam=:s",
            ExpressionAttributeValues={
                ':s': True
            },
            ReturnValues="UPDATED_NEW"
        )"""
        tweet.isSpam = True

    def run(self, tweet):
        classifyResult = self.spamSet.classifyTweet(tweet.preprocessedTweet)

        if classifyResult:
            self.setAsSpam(tweet)

