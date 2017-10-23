#from Databases import Database
from nltk.tag.stanford import StanfordPOSTagger
from nltk.stem import WordNetLemmatizer
from nltk.parse import stanford
import os
from nltk.parse.stanford import StanfordParser
import re

class InstanceTweet:
    def __init__(self, tweet):
        self.tweet = tweet
        self.emoji = []
        self.tweetTokenized = []
        self.tweetLemmatized = []
        self.tweetTree = []

    def emojiExtractor(self, tweet):
        self.emoji = re.findall(":\w+:", tweet)
        for character in self.emoji:
            if character == " ":
                return tweet
        self.tweet = " ".join(re.sub(r":\w+:",'',tweet).split())









def run():
    java_path = "C:\ProgrA~1\Java\jdk1.8.0_151"
    os.environ['JAVAHOME'] = java_path
    os.environ['STANFORD_PARSER'] = 'C:\Progra~1\stanford-parser-full-2017-06-09\stanford-parser.jar'
    os.environ['STANFORD_MODELS'] = 'C:\Progra~1\stanford-parser-full-2017-06-09\stanford-parser-3.8.0-models.jar'
    model_path = 'C:\Progra~1\stanford-parser-full-2017-06-09\englishPCFG.ser.gz'
    parser = stanford.StanfordParser(model_path=model_path)
    parser = StanfordParser('C:\Progra~1\stanford-parser-full-2017-06-09\stanford-parser.jar','C:\Progra~1\stanford-parser-full-2017-06-09\stanford-parser-3.8.0-models.jar')


    qallTweets= []
    tweetList = ["I'm going to the market to buy vegetables and some very fresh fruits.", 'He are very smart', "bababa bababa :rola_check: babab"]
    allTweets = [InstanceTweet(tweet) for tweet in tweetList]
    #TODO -> Identificar emoji em tweets(tokens que começam e terminam com ':' e tem mais de uma posicao)
    st = StanfordPOSTagger('C:\Progra~1\stanford-postagger\models\english-bidirectional-distsim.tagger','C:\Progra~1\stanford-postagger\stanford-postagger.jar')
    lemmatizer = WordNetLemmatizer()
    for indexTweet, tweet in enumerate(allTweets):
        #EmojiExtractor
        tweet.emojiExtractor(tweet.tweet)
        #Transforma tweets em tokens
        tweet.tweetTokenized = st.tag(tweet.tweet.split())
        #faz a lemmatizacao das palavras
        for word in tweet.tweet.split():
            tweet.tweetLemmatized.append(lemmatizer.lemmatize(word, 'v'))
            #tweet.tweetLemmatized.append(lemmatizer.lemmatize(word, 'n'))
        #Transforma as palavras lemmatizadas em uma unica string
        tweet.tweetLemmatized = " ".join(tweet.tweetLemmatized)
        #Seta a arvore do tweet no objeto
        tweet.tweetTree = list(parser.raw_parse(tweet.tweetLemmatized))
        """#Interface tweetTree para demonstracao
        for line in sentence:
            for sentence in line:
                sentence.draw()"""
        print(tweet.tweetLemmatized)


 #return sentiments

run()