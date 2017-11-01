import emoji
import re


class Emojinator(object):

    def get_emoji_list(self, text):
        text = emoji.demojize(text, delimiters=(" :", ": "))
        emoji_list = re.findall(":(?:\w|-|\&)+:", text)
        text = re.sub(':(?:\w|-|\&)+:', ' ', text)

        return text, emoji_list
