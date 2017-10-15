from Databases import Database


def run():

    sentiments = [{"happy": 0.5}, {"sad": 0.01}]

    allTweets = Database.getAll(Database.rawTweets)

    for tweet in allTweets:
        # TODO -> JUST DO IT! MAKE THOSE SENTIMENT COME TRUE!
        tweet

    return sentiments