from senticnet.senticnet import Senticnet

class SenticNet(object):

    def getInfo(self, concept):
        try:
            sn = Senticnet()
            concept_info = sn.concept(concept)
            polarity_value = sn.polarity_value(concept)
            polarity_intense = sn.polarity_intense(concept)
            moodtags = sn.moodtags(concept)
            semantics = sn.semantics(concept)
            sentics = sn.sentics(concept)

            """print(concept)
            print("concept_info: {}".format(concept_info))
            print("polarity_value: {}".format(polarity_value))
            print("polarity_intense: {}".format(polarity_intense))
            print("moodtags: {}".format(moodtags))
            print("semantics: {}".format(semantics))
            print("sentics: {}".format(sentics))
            print("\n\n")"""
            return "{} - {}".format(polarity_value, polarity_intense)
        except:
            return "NOT POSSIBLE"

    def getInfoList(self, concepts):
        infos = []
        for concept in concepts:
            info = self.getInfo(concept)
            infos.append(info)
            print("{}: {}".format(concept, info))
        return infos
