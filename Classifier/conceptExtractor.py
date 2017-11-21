import os
import nltk
from nltk.corpus import wordnet
from nltk.parse.stanford import StanfordParser
from nltk.stem import WordNetLemmatizer


class ConceptExtractor(object):
    def __init__(self):
        java_path = "C:\Program Files (x86)\Java\jdk1.8.0_152"
        os.environ['JAVAHOME'] = java_path

        parser_jar_path = 'Classifier/binaries/stanford-parser.jar'
        parser_models_path = 'Classifier/binaries/stanford-parser-3.8.0-models.jar'
        self.parser = StanfordParser(parser_jar_path, parser_models_path)

        self.stop_words = []
        file = open('SpamFilter/binaries/stopwords.txt', 'r')
        for line in file:
            line = line.strip("\n")
            self.stop_words.append(line)

        self.lemmatizer = WordNetLemmatizer()

        self.ADJ = ["JJ", "JJR", "JJS"]
        self.NOUN = ["NN", "NNS", "NNP", "NNPS"]
        self.VERB = ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]

    def extract_list_of_event_concepts(self,
                                       tweet_text="Game Of Thrones is awesome"):
        # print("text: " + tweet_text)

        list_of_concepts = []
        list_of_np_and_parent_nodes = []
        tweet_tree = list(self.parser.raw_parse(tweet_text))[0]
        # tweet_tree.draw()
        sentence_list = list(tweet_tree.subtrees(lambda x: (x.label().startswith("S") and x.label() != "SYM")))
        # print("number of sentences" + str(len(sentence_list)))
        if len(sentence_list) != 0:
            for sentence in sentence_list:
                ""
                # print(sentence)
            for sentence in sentence_list:
                list_of_np_and_parent_nodes.extend(self.get_list_of_np_and_parents(sentence, [], []))
        else:
            list_of_np_and_parent_nodes.extend(self.get_list_of_np_and_parents(tweet_tree, [], []))

        # print(list_of_np_and_parent_nodes)
        list_of_np_and_verbs = [self.get_np_and_verb(np) for np in list_of_np_and_parent_nodes]
        lemmatized_list_of_np_and_verbs = []
        for np, verb in list_of_np_and_verbs:
            if len(np) > 0 and len(verb) > 0:
                lemmatized_nouns = []
                for noun in np:
                    noun_tag = self.get_wordnet_pos(noun[1])
                    if noun_tag is not None:
                        lemmatized_nouns.append((
                            self.lemmatizer.lemmatize(noun[0], noun_tag),
                            noun[1]
                        ))
                    else:
                        lemmatized_nouns.append((
                            self.lemmatizer.lemmatize(noun[0]),
                            noun[1]
                        ))
                lemmatized_list_of_np_and_verbs.append((
                    lemmatized_nouns,
                    self.lemmatizer.lemmatize(verb[0], self.get_wordnet_pos(verb[1])))
                )

        for np, verb in lemmatized_list_of_np_and_verbs:
            object_concepts = self.extract_list_of_object_concepts(np)
            for object_concept in object_concepts:
                list_of_concepts.append(verb + "_" + object_concept)

        # print("list of concepts: " + str(list_of_concepts))
        return list_of_concepts

    def extract_list_of_object_concepts(self, noun_phrase):
        '''noun_phrase = list of tuples in the format (word, pos_tag)'''
        list_of_object_concepts = []
        if len(noun_phrase) == 1:
            if noun_phrase[0][1] in self.ADJ or noun_phrase[0][1] in self.NOUN:
                list_of_object_concepts.append(noun_phrase[0][0])
        else:
            for index, word in enumerate(noun_phrase):
                if index < len(noun_phrase) - 1:
                    bigram = [word, noun_phrase[index + 1]]
                    if not (bigram[0][0] in self.stop_words and bigram[1][0] in self.stop_words):
                        if (bigram[0][1] in self.ADJ) and (bigram[1][1] in self.NOUN):
                            list_of_object_concepts.append(bigram[0][0] + "_" + bigram[1][0])
                            list_of_object_concepts.append(bigram[1][0])
                        elif (bigram[0][1] in self.NOUN) and (bigram[1][1] in self.NOUN):
                            list_of_object_concepts.append(bigram[0][0] + "_" + bigram[1][0])
                        elif (bigram[0][0] in self.stop_words) and (bigram[1][1] in self.NOUN):
                            list_of_object_concepts.append(bigram[1][0])
                        elif (bigram[0][1] in self.NOUN) and (bigram[1][0] in self.stop_words):
                            list_of_object_concepts.append(bigram[0][0])
                        elif not (bigram[0][1] in self.ADJ and (bigram[1][0] in self.stop_words)) and not (
                                        bigram[0][0] in self.stop_words and (bigram[1][1] in self.ADJ)):
                            list_of_object_concepts.append(bigram[0][0] + "_" + bigram[1][0])

                            # print(list_of_object_concepts)
        return list_of_object_concepts

    def get_list_of_np_and_parents(self, sentence_tree, np_and_parents=[], parent_stack=[]):
        parent_stack.append(sentence_tree)
        for subtree in sentence_tree:
            if not isinstance(subtree, str):
                if subtree.label() == "NP":
                    aux_stack = list(parent_stack)  # list function is used to create a copy of parent stack
                    parent = aux_stack.pop()
                    while parent.label() != "VP" and \
                            not (parent.label().startswith("S") and parent.label() != "SYM") \
                            and parent.label() != "ROOT":
                        parent = aux_stack.pop()
                    np_and_parents.append((subtree, parent))
                # keep searching the tree until you find a new sentence
                elif not (subtree.label().startswith("S") and subtree.label() != "SYM"):
                    self.get_list_of_np_and_parents(subtree, np_and_parents, parent_stack)
        parent_stack.pop()
        return np_and_parents

    def get_np_and_verb(self, np):
        np_pos = self.find_np_pos(np[0], [])
        verb = self.find_verb(np[1], "")

        return np_pos, verb

    def find_np_pos(self, np, list_of_pos_tags):
        for subtree in np:
            if isinstance(subtree[0], str):
                list_of_pos_tags.append((subtree[0],
                                         subtree.label()))
            elif subtree.label().startswith("S") and subtree.label() != "SYM":
                self.find_np_pos(subtree, list_of_pos_tags)

        return list_of_pos_tags

    def find_verb(self, vp, verb):
        if verb == "":
            for subtree in vp:
                if verb == "":
                    if not isinstance(subtree, str):
                        if subtree.label() in self.VERB:
                            verb = (subtree[0], subtree.label())
                        elif subtree.label().startswith("S") and subtree.label() != "SYM":
                            verb = self.find_verb(subtree, verb)
        return verb

    def get_wordnet_pos(self, pos_tag):
        if pos_tag.startswith('J'):
            return wordnet.ADJ
        elif pos_tag.startswith('V'):
            return wordnet.VERB
        elif pos_tag.startswith('N'):
            return wordnet.NOUN
        elif pos_tag.startswith('R'):
            return wordnet.ADV
        else:
            return None
