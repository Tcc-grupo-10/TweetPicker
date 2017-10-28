from senticnet.senticnet import Senticnet

def getInfo(concept):
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

def getInfoList(concepts):
    for concept in concepts:
        info = getInfo(concept)
        print("{}: {}".format(concept, info))

getInfoList(["go_market", "fresh_fruit", "bad_feeling", "dont_know"])