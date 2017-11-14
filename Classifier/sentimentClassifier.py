from Classifier.conceptExtractor import ConceptExtractor
from Classifier.SenticNet import SenticNet
from Emojinator import Emojinator


class SentimentClassifier(object):

    def __init__(self):
        self.senticNet = SenticNet()
        self.emojinator = Emojinator()

    def run(self, tweet):
        # concept_extractor = ConceptExtractor()
        #tweet = "i just love brown. gots7"
        # concept_extractor.extract_list_of_event_concepts(tweet.preprocessedTweet)
        #concept_extractor.extract_list_of_object_concepts()

        # TODO -> get concepts from concept_extractor
        concepts = ["go_market", "fresh_fruit", "bad_feeling", "dont_know"]

        sentic_net_sentiments = self.senticNet.getInfoList(concepts)
        # emojis_sentiments = self.emojinator.get_feelings(tweet.emojis)
        emojis_sentiments = self.emojinator.get_feelings([":thumbs_up:", ":hushed_face:", ":broken_heart:"])

        calc_sentiments = self.calc_feelings(sentic_net_sentiments, emojis_sentiments)
        print("calc_sentiments: {}".format(calc_sentiments))
        return calc_sentiments

    def calc_feelings(self, sentic_net, emojis):

        emojisAvg = 0
        if len(emojis) > 0:
            emojisAvg = sum(emojis) / float(len(emojis))

        snAvg = self.senticNet.getAvg(sentic_net)

        if snAvg is None:
            return None
        else:
            snAvg["emoji"] = emojisAvg
            return snAvg
