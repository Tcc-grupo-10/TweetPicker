# from Databases import Database
from Services.SpamSet import SpamSet

class SpamFiltering(object):

    def __init__(self):
        self.spamSet = SpamSet()

    def setAsSpam(self, tweet_id):
        """Database.rawTweets.update_item(
            Key={'tweet_id': tweet_id},
            UpdateExpression="set is_spam=:s",
            ExpressionAttributeValues={
                ':s': True
            },
            ReturnValues="UPDATED_NEW"
        )"""

    def run(self, tweet):
        classifyResult = self.spamSet.classifyTweet(tweet.preprocessedTweet)
        isSpam = self.thisIsSpam(classifyResult)

        """if isSpam:
            setAsSpam(tweet["tweet_id"])"""

    def thisIsSpam(self, classifyResult):
        # print(classifyResult)
        return False
