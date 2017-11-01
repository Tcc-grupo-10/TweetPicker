import re
import xml

from unidecode import unidecode
from Emojinator import Emojinator


class PreProcessor(object):
    def __init__(self, run_id,  db):
        self._db = db
        self._emojinator = Emojinator()

    def pre_process_tweet(self, tweet):

        (tweet_text, emojis) = self._emojinator.get_emoji_list(tweet.original_tweet)

        tweet_text = unidecode(tweet_text)
        tweet_text = tweet_text.lower()

        tweet_text = self.remove_URL(tweet_text)
        tweet_text = self.remove_white_spaces_excess(tweet_text)
        tweet_text = self.remove_hashtags(tweet_text)
        tweet_text = self.remove_users(tweet_text)

        # Removing HTML tags
        tweet_text = self.removeTags(tweet_text)

        # Replacing unknown chars
        tweet_text = tweet_text.replace('[?]', '')
        tweet_text = tweet_text.replace('&amp;', '&')
        tweet_text = tweet_text.replace('&lt;', '<')
        tweet_text = tweet_text.replace('&gt;', '>')


        tweet_text = self.use_white_spaces_as_delimiters(tweet_text)

        tweet.preprocessed_tweet = tweet_text
        tweet.emojis = emojis

        self._db.save_preprocessed_tweet(tweet)

    def remove_users(self, text):
        text = re.sub('@[^\s]+', 'AT_USER', text)
        return text

    def remove_hashtags(self, text):
        # Replace #word with word
        text = re.sub(r'#([^\s]+)', r'\1', text)
        return text

    def remove_URL(self, text):
        tweet = re.sub('((www\.[^\s]+)|(https?:/[^\s]+))', '', text)
        return tweet

    def use_white_spaces_as_delimiters(self, text):
        # Insere espacos entre os caracteres da variavel tokenPunctuation para nao interferir no lemmatize
        tokenPunctuation = r"""!.,;()+"""
        text = text.translate(str.maketrans({key: " {0} ".format(key) for key in tokenPunctuation}))
        return text

    def remove_white_spaces_excess(self, text):
        text = text.replace('\n', ' ')
        text = text.strip()
        text = re.sub('[\s]+', ' ', text)

        return text

    def removeTags(self, text):
        try:
            text = ''.join(xml.etree.ElementTree.fromstring("<p>" + text + "</p>").itertext())
        finally:
            return text