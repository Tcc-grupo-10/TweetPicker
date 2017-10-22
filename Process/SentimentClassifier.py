#from Databases import Database
#from Services import WordClassifier
from nltk.tokenize import TweetTokenizer
from nltk import pos_tag
from nltk.tag.stanford import StanfordPOSTagger
import os


def run():
    java_path = "C:\ProgrA~1\Java\jdk1.8.0_151"
    os.environ['JAVAHOME'] = java_path
   # sentiments = [{"happy": 0.5}, {"sad": 0.01}]

    #allTweets = Database.getAll(Database.rawTweets)
    allTweets = "I am going to the market to buy vegetables and some fruits"


    st = StanfordPOSTagger('C:\Progra~1\stanford-postagger\models\english-bidirectional-distsim.tagger','C:\Progra~1\stanford-postagger\stanford-postagger.jar')
    print(st.tag(allTweets.split()))
    



    #return sentiments

run()