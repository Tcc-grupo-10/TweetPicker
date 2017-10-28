import emoji
import csv


def get_csv_values():
    ret = {}
    with open('../Etc/Emoji_Sentiment_Data_v1.1.csv', 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            score = float(row["Sentiment Score"]) / 1000

            ret[row["Emoji"]] = score
    return ret


class SentimentFromEmoji:

    def __init__(self):
        self.emojiFeelings = get_csv_values()

    def get_feeling(self, emojiStr):
        emoj = emoji.emojize(emojiStr)

        sentiment = self.emojiFeelings[emoj]
        print("{} -> {}".format(emoj, sentiment))
        return sentiment

    def get_feelings(self, emojis):
        for emojiStr in emojis:
            self.get_feeling(emojiStr)

emojisTest = [":winking_face:", ":face_screaming_in_fear:", ":princess:", ":loudly_crying_face:", ":broken_heart:"]
SentimentFromEmoji().get_feelings(emojisTest)