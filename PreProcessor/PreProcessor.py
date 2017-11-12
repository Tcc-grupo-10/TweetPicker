import re
import xml

from unidecode import unidecode

from Emojinator import Emojinator


class PreProcessor(object):
    def __init__(self):
        self._emojinator = Emojinator()

    def pre_process_tweet(self, raw_text):

        (pre_processed_text, emojis) = self._emojinator.get_emoji_list(raw_text)

        pre_processed_text = unidecode(pre_processed_text)
        pre_processed_text = pre_processed_text.lower()

        pre_processed_text = self.remove_URL(pre_processed_text)
        pre_processed_text = self.remove_white_spaces_excess(pre_processed_text)
        pre_processed_text = self.remove_hashtags(pre_processed_text)
        pre_processed_text = self.remove_users(pre_processed_text)

        # Removing HTML tags
        pre_processed_text = self.removeTags(pre_processed_text)

        # Replacing unknown chars
        pre_processed_text = pre_processed_text.replace('[?]', '')
        pre_processed_text = pre_processed_text.replace('&amp;', '&')
        pre_processed_text = pre_processed_text.replace('&lt;', '<')
        pre_processed_text = pre_processed_text.replace('&gt;', '>')

        pre_processed_text = self.use_white_spaces_as_delimiters(pre_processed_text)

        return pre_processed_text, emojis


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
