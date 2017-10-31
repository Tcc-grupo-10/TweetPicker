#from Databases import Database
from Services import SpamSet

class SpamFiltering(object):

    def __init__(self):
        self.spamSet = SpamSet.SpamSet()

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
        classifyResult = self.spamSet.classifyTweet(tweet["clear_text"])
        isSpam = self.thisIsSpam(classifyResult)

        """if isSpam:
            setAsSpam(tweet["tweet_id"])"""

        # TODO -> Atualizar para filtrar os com spam

    def thisIsSpam(self, classifyResult):
        print(classifyResult)
        return False
