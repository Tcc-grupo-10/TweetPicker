"""
um apontador por início do n-grama, um apontador pro final

enquanto o que está apontando pro início é uma stop word, move o apontador do início
quando encontrar alguém que não é stop word, o apontador do end recebe o do começo
enquanto não tiver n palavras, move o apontador do end pra frente
se for stop word, pula
se não for, acrescenta no n-grama
"""


def getAllFeatures(training_tweets, stopwords=, grams, min_frequency):
    n_grams = {}

    for tweet in training_tweets:
        beginning = 0
        tweet_words = list(tweet.keys())[0].split(" ")
        gram_holder = []

        while beginning < len(tweet_words):
            while tweet_words[beginning] in stopwords and beginning < len(tweet_words) - 1:
                beginning += 1
            end = beginning
            gram_holder.append(tweet_words[beginning])

            while len(gram_holder) < grams and end < len(tweet_words) - 1:
                end += 1
                if tweet_words[end] not in stopwords:
                    gram_holder.append(tweet_words[end])

            if len(gram_holder) == grams:
                full_gram = " ".join(gram_holder)
                n_grams[full_gram] = n_grams.get(full_gram, 0) + 1

            gram_holder = []
            beginning += 1

    filtered_n_gram = []
    for gram in n_grams:
        if n_grams[gram] >= min_frequency:
            filtered_n_gram.append(gram)

    return filtered_n_gram

getAllFeatures(({"simple tweet with text": True}, {"Another text words about nothing this simple": True}, {"something about this simple tweet": False}))

def getTweetFeatureVector(tweet, feature_list):
    features = []
    for feature in feature_list:
        if feature in tweet:
            features.append(feature)