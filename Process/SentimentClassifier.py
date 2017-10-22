#from Databases import Database
#from Services import WordClassifier
from nltk.tokenize import TweetTokenizer
from nltk import pos_tag

def run(allTweets):

   # sentiments = [{"happy": 0.5}, {"sad": 0.01}]

#    allTweets = Database.getAll(Database.rawTweets)
    allTweets = {"I am going to the market to buy vegetables and some fruits", "sad sad"}
    tknzr = TweetTokenizer()
    for tweet in allTweets:
        # TODO -> JUST DO IT! MAKE THOSE SENTIMENT COME TRUE!
        tokens = pos_tag(tknzr.tokenize(tweet))
        print (tokens)

    #return sentiments

run()