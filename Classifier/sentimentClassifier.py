from Classifier.conceptExtractor import ConceptExtractor

class SentimentClassifier(object):

    def run(self, tweet):
        concept_extractor = ConceptExtractor()
        #tweet = "i just love brown. gots7"
        tweet.sentiment = concept_extractor.extract_list_of_event_concepts(tweet.preprocessedTweet)
        #concept_extractor.extract_list_of_object_concepts()

# run()
