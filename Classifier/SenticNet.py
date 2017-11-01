from senticnet.senticnet import Senticnet

class SenticNet(object):

    def getInfo(self, concept):
        try:
            sn = Senticnet()
            polarity_value = sn.polarity_value(concept)
            polarity_intense = sn.polarity_intense(concept)
            sentics = sn.sentics(concept)

            sentics["polarity_value"] = polarity_value
            sentics["polarity_intense"] = polarity_intense

            return sentics
        except:
            return {'pleasantness': '0.0', 'attention': '0.0', 'sensitivity': '0.0', 'aptitude': '0.0', 'polarity_value': 'neutral', 'polarity_intense': '0.0'}

    def getInfoList(self, concepts):
        infos = []
        for concept in concepts:
            info = self.getInfo(concept)
            infos.append(info)
            print("{}: {}".format(concept, info))
        return infos
