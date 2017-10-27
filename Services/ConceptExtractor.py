from nltk.tag.stanford import StanfordPOSTagger
from nltk.stem import WordNetLemmatizer
import os
from nltk.parse.stanford import StanfordParser
import re
from nltk.corpus import wordnet

class InstanceTweet:
    def __init__(self, text):
        self.text = text
        self.intact = text
        self.emoji = []
        self.tweetTokenized = []
        self.tweetLemmatized = []
        self.tweetTree = []
        self.ngram = []

    def emojiExtractor(self, text):
        self.emoji = re.findall(":\w+:", text)
        for character in self.emoji:
            if character == " ":
                return text
        self.text = " ".join(re.sub(r":\w+:", '', text).split())


def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return None


def run():
    # Variaveis de ambiente necessarias!
    #===============================================================================================================
    #Local do Java JDK (Sim, precisa instalar o JDK)
    java_path = "C:\ProgrA~1\Java\jdk1.8.0_151"
    os.environ['JAVAHOME'] = java_path
    #Localizar os .jar's do stanfordParser
    parser = StanfordParser('C:\Progra~1\stanford-parser-full-2017-06-09\stanford-parser.jar',
                            'C:\Progra~1\stanford-parser-full-2017-06-09\stanford-parser-3.8.0-models.jar')
    #Localizar o engish tagger e o .jar do stanfordPOSTagger
    st = StanfordPOSTagger('C:\Progra~1\stanford-postagger\models\english-bidirectional-distsim.tagger',
                           'C:\Progra~1\stanford-postagger\stanford-postagger.jar')
    lemmatizer = WordNetLemmatizer()
    # ===============================================================================================================
    #String para adicionar espaços entre os caracteres contidos nela
    tokenPunctuation = r"""!.,;()+"""
    #Tweets que serão utilizados
    tweetList = ["I am going to buy some fruits and some vegetables.","Segundo tweet", "Terceiro Tweet"]
    #Todas as strings da Lista de strings tweetList serão instanciadas na lista de objetos allTweets
    allTweets = [InstanceTweet(tweet) for tweet in tweetList]
    #Para todos as strings do objectList allTweets:
    for tweet in allTweets:
        # Extrai emojis e guarda no objeto.emoji
        tweet.emojiExtractor(tweet.text)
        #Insere espacos entre os caracteres da variavel tokenPunctuation para nao interferir no lemmatize
        tweet.text = tweet.text.translate(str.maketrans({key: " {0} ".format(key) for key in tokenPunctuation}))
        # Transforma tweets em tuplas [palavra,Tag referente a palavra] para cada palavra/caractere contida na string. Lista de tags está no documento 'Analise de Sentimento - SenticComputing - ConceptExtractor.docx' da Aline.
        tweet.tweetTokenized = st.tag(tweet.text.split())
        #Faz a lemmatizacao das palavras para cada tupla na lista de tuplas do tweetTokenized
        for word, tag in tweet.tweetTokenized:
            #Determina função da palavra na frase de acordo com sua tag de acordo com o metodo get_wordnet_pos()
            wntag = get_wordnet_pos(tag)
            #Apenas ADV, NOUN, VERB e ADJ devem ser informados como segundo parametro. Caso não seja nenhum desses casos, o segundo parametro deverá ser None.
            if wntag is None:  # not supply tag in case of None
                tweet.tweetLemmatized.append(lemmatizer.lemmatize(word))
            else:
                tweet.tweetLemmatized.append(lemmatizer.lemmatize(word, pos=wntag))
        # Transforma a lista de palavras lemmatizadas em uma unica string
        tweet.tweetLemmatized = " ".join(tweet.tweetLemmatized)
        # Faz um cast da arvore retornada para o tipo List e a insere no objeto
        tweet.tweetTree = list(parser.raw_parse(tweet.tweetLemmatized))[0]
        #Função mágica que consegue pegar nós da arvore referente ao seu label no filter de lambda
        tweet.tweetTree = [[" ".join(vp.leaves()), "".join(vp.label())] for vp in list(tweet.tweetTree.subtrees(filter=lambda x:  x.label() == 'NP'))]

        #Criação de bigramas para utilizar nos resultados obtidos com o chunk da tweetTree
        #Cria string com palavras da tweetTree para o bigram
        """
        nounphrase = ''
        for np,token in tweet.tweetTree:
            #if np not in nounphrase:
            nounphrase += " " + np


        bigrams = ngrams(nounphrase.split(),2)

        for grams in bigrams:
            print(grams)
        """
        # Interface tweetTree para ilustração da arvore
        """for line in tweet.tweetTree:
            for tweet.tweetTree in line:
                tweet.tweetTree.draw()"""
    return allTweets

#Inicializa o método run()
run()