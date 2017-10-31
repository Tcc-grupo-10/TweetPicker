from Classifier.conceptExtractor import ConceptExtractor
from Services.SenticNet import SenticNet

class SentimentClassifier(object):

    def __init__(self):
        self.senticNet = SenticNet()

    def run(self, tweet):
        concept_extractor = ConceptExtractor()
        #tweet = "i just love brown. gots7"
        concept_extractor.extract_list_of_event_concepts(tweet.preprocessedTweet)
        #concept_extractor.extract_list_of_object_concepts()

        # TODO -> get concepts from concept_extractor
        concepts = ["go_market", "fresh_fruit", "bad_feeling", "dont_know"]

        tweet.sentiment = self.senticNet.getInfoList(concepts)

# run()
