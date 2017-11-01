import emoji
import re
import csv


class Emojinator(object):

    def __init__(self):
        self.emojiFeelings = self.get_csv_values()

    def get_emoji_list(self, text):
        text = emoji.demojize(text, delimiters=(" :", ": "))
        emoji_list = re.findall(":(?:\w|-|\&)+:", text)
        text = re.sub(':(?:\w|-|\&)+:', ' ', text)

        return text, emoji_list

    def get_csv_values(self):
        ret = {}
        with open('Etc/Emoji_Sentiment_Data_v1.1.csv', 'r', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                score = float(row["Sentiment Score"]) / 1000

                ret[row["Emoji"]] = score
        return ret

    def get_feeling(self, emojiStr):
        emoj = emoji.emojize(emojiStr)

        sentiment = self.emojiFeelings[emoj]
        print("{} -> {}".format(emoj, sentiment))
        return sentiment

    def get_feelings(self, emojis):
        feelings = []
        for emojiStr in emojis:
            feelings.append(self.get_feeling(emojiStr))
        return feelings