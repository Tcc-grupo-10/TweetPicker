#from Databases import Database
from nltk.tag.stanford import StanfordPOSTagger
import os
from nltk.stem import WordNetLemmatizer



def run(allTweets):
    java_path = "C:\ProgrA~1\Java\jdk1.8.0_151"
    os.environ['JAVAHOME'] = java_path


    #allTweets = Database.getAll(Database.rawTweets)

    #TODO -> Identificar emoji em tweets(tokens que começam e terminam com ':' e tem mais de uma posicao)
    st = StanfordPOSTagger('C:\Progra~1\stanford-postagger\models\english-bidirectional-distsim.tagger','C:\Progra~1\stanford-postagger\stanford-postagger.jar')
    lemmatizer = WordNetLemmatizer()
    for tweet in allTweets:
        tweet = st.tag(tweet.split())
        for word in tweet:
            tweetLemmatized = lemmatizer.lemmatize(word[0])






    #return sentiments

