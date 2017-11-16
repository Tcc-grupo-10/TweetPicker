from senticnet.senticnet import Senticnet


class SenticNet(object):

    def getInfo(self, concept):
        try:
            sn = Senticnet()
            polarity_intense = sn.polarity_intense(concept)
            sentics = sn.sentics(concept)
            sentics["polarity_intense"] = polarity_intense
            sentics["searched_concept"] = concept

            return sentics
        except:
            split_words = list(filter(lambda x: x != concept, concept.split("_")))
            returned_sentiments = []

            for word in split_words:
                word_sentiment = self.getInfo(word)
                if word_sentiment is not None:
                    returned_sentiments.append(word_sentiment)

            if len(returned_sentiments) == 0:
                return None
            else:
                avg = self.getAvg(returned_sentiments)
                return avg

    def getInfoList(self, concepts):
        infos = []
        for concept in concepts:
            info = self.getInfo(concept)
            infos.append(info)
        return infos

    def getAvg(self, concepts):

        sentiment_avg = {'pleasantness': 0.0, 'attention': 0.0, 'sensitivity': 0.0,
                         'aptitude': 0.0, 'polarity_intense': 0.0, "searched_concept": ""}

        sentic_filtered = list(filter(lambda x: x is not None, concepts))

        for sentic in sentic_filtered:
            sentiment_avg['pleasantness'] += float(sentic['pleasantness'])
            sentiment_avg['attention'] += float(sentic['attention'])
            sentiment_avg['sensitivity'] += float(sentic['sensitivity'])
            sentiment_avg['aptitude'] += float(sentic['aptitude'])
            sentiment_avg['polarity_intense'] += float(sentic['polarity_intense'])
            sentiment_avg['searched_concept'] += ", {}".format(sentic['searched_concept'])

        if len(sentic_filtered) > 0:
            sentiment_avg['pleasantness'] /= float(len(sentic_filtered))
            sentiment_avg['attention'] /= float(len(sentic_filtered))
            sentiment_avg['sensitivity'] /= float(len(sentic_filtered))
            sentiment_avg['aptitude'] /= float(len(sentic_filtered))
            sentiment_avg['polarity_intense'] /= float(len(sentic_filtered))
            sentiment_avg['searched_concept'] = sentiment_avg['searched_concept'].replace(", ", "", 1)
            return sentiment_avg
        else:
            return None
