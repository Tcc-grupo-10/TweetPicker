import concurrent.futures
import csv
import datetime
import multiprocessing

import _thread
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC

from DataFormatter.DataFormatter import DataFormatter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

from PreProcessor.PreProcessor import PreProcessor
from SpamFilter import Tools


class SpamSet(object):
    def __init__(self, useStopwords=True, nGram=2, frequencyMin=1):

        print("Inicio: {}".format(datetime.datetime.now()))

        self.featureVector = []
        self.tweets = []
        self.frequencyMin = frequencyMin
        self.nGram = nGram
        self.useStopwords = useStopwords
        self.stopwords = Tools.getStopwords(useStopwords)

        self.preProcessing = PreProcessor()
        self.dataFormatter = DataFormatter()

        self.trainData = []
        self.testData = []

        self.load_test_csv()
        self.load_train_csv()

        self.queue = None
        self.csv_file_writer = None

        # predict vars
        self.train_set = []
        self.isSpamList = []
        self.X_train_counts = None
        self.count_vect = CountVectorizer()
        self.tfidf_transformer = TfidfTransformer()

        self.learn()

    def learn(self):

        print("Aprendendo: {}".format(datetime.datetime.now()))

        featureVectorCount = {}
        for (text, label) in self.trainData:
            tweetFV = Tools.getFeatureVector(text, self.nGram, self.stopwords)
            self.featureVector = Tools.updateVector(tweetFV, featureVectorCount)
            self.tweets.append(tweetFV)
            self.isSpamList.append(label)
        print("featureVectorCount: {}".format(datetime.datetime.now()))

        featureVectorCount = Tools.removeFrequencyFromVector(self.frequencyMin, featureVectorCount)
        print("Feature Vector Count: {}".format(datetime.datetime.now()))

        self.featureVector = Tools.getVectorWithoutCount(featureVectorCount)
        self.tweets = Tools.removeFrequencyFromTweets(self.featureVector, self.tweets)
        print("Removing Frequency From Tweets: {}".format(datetime.datetime.now()))

        self.X_train_counts = self.count_vect.fit_transform(self.tweets)
        print("X_train_counts Done: {}".format(datetime.datetime.now()))
        self.train_set = self.tfidf_transformer.fit_transform(self.X_train_counts)
        print("train_set Done: {}".format(datetime.datetime.now()))

        print("Aprendeu: {}".format(datetime.datetime.now()))

    def predict_nb(self, text):
        docs_processed = [Tools.getTweetFeatureVector(text, self.featureVector)]

        X_new_counts = self.count_vect.transform(docs_processed)
        X_new_tfidf = self.tfidf_transformer.transform(X_new_counts)

        clf = MultinomialNB().fit(self.train_set, self.isSpamList)
        predicted = clf.predict(X_new_tfidf)

        return predicted[0]

    def predict_svm(self, text):
        docs_processed = [Tools.getTweetFeatureVector(text, self.featureVector)]

        X_new_counts = self.count_vect.transform(docs_processed)
        X_new_tfidf = self.tfidf_transformer.transform(X_new_counts)

        clf = SVC().fit(self.train_set, self.isSpamList)
        predicted = clf.predict(X_new_tfidf)

        return predicted[0]

    def predict_all(self):
        m = multiprocessing.Manager()
        self.queue = m.Queue()
        _thread.start_new_thread(self.queue_worker, ())

        executor = concurrent.futures.ProcessPoolExecutor(10)
        futures = [executor.submit(self.predict_item, item) for item in enumerate(self.testData)]
        concurrent.futures.wait(futures)

    def predict_item(self, tweet):
        nb = self.predict_nb(tweet[1][0])
        svm = self.predict_svm(tweet[1][0])
        print("{} - original: {}| nb: {}| svm: {}".format(tweet[0], tweet[1][1], nb, svm))
        self.queue.put((tweet[1], nb, svm))

    def save_in_csv(self, tweet_results, file_writer):
        file_writer.writerow([tweet_results[0][2],
                              tweet_results[0][0],
                              tweet_results[0][1],
                              tweet_results[1],
                              tweet_results[2]])

    def queue_worker(self):
        file_name = '../Etc/sw_{}_ng_{}_fr_{}.csv'.format(self.useStopwords, self.nGram, self.frequencyMin)
        file_writer = csv.writer(open(file_name, 'w', newline=''))
        while True:
            try:
                if not self.queue.empty():
                    item = self.queue.get()
                    if item is None:
                        break
                    self.save_in_csv(item, file_writer)
                    self.queue.task_done()
            except:
                print("Queue Error!!!!!")
                break

    def load_test_csv(self):
        with open('../Etc/teste.csv', 'rt', encoding="utf8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                id = row["tweet_id"].strip()
                text = row["text"].strip()
                label = row["label"].strip()

                (text, emojis) = self.preProcessing.pre_process_tweet(text)
                text = self.dataFormatter.format_data(text)

                self.testData.append((text, label, id))

    def load_train_csv(self):
        with open('../Etc/treino.csv', 'rt', encoding="utf8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                text = row["text"].strip()
                label = row["label"].strip()

                (text, emojis) = self.preProcessing.pre_process_tweet(text)
                text = self.dataFormatter.format_data(text)

                self.trainData.append((text, label))


ss = SpamSet()
ss.predict_all()

print("Fim: {}".format(datetime.datetime.now()))
