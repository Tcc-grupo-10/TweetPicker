import re
import os
import http.client
import urllib.parse
import json

class SpellCheck(object):
    """
    # Converte Tokens em uma string.
    def untokenize(tokens):
        text = ' '.join(tokens)
        step1 = text.replace("`` ", '"').replace(" ''", '"').replace('. . .', '...')
        step2 = step1.replace(" ( ", " (").replace(" ) ", ") ")
        step3 = re.sub(r' ([.,:;?!%]+)([ \'"`])', r"\1\2", step2)
        step4 = re.sub(r' ([.,:];?!%]+)$', r"\1", step3)
        step5 = step4.replace(" '", "'").replace(" n't", "n't").replace("can not", "cannot")
        step6 = step5.replace(" ` ", " '")
        text = step6.strip()
        return text
    """
    # Corrige erros gramaticais
    def azureSpellCheck(self, tweet):
        azure_key = os.environ['azure_key']

        params = {'mkt': 'en-US', 'mode': 'spell', 'text': tweet}
        # NOTE: Replace this example key with a valid subscription key.
        key = azure_key
        host = 'api.cognitive.microsoft.com'
        path = '/bing/v7.0/spellcheck'
        headers = {'Ocp-Apim-Subscription-Key': key,
                   'Content-Type': 'application/x-www-form-urlencoded'}
        conn = http.client.HTTPSConnection(host)
        params = urllib.parse.urlencode(params)
        conn.request("POST", path, params, headers)
        response = conn.getresponse()
        suggestions = json.loads(response.read())
        for indexSugg, suggestion in enumerate(suggestions["flaggedTokens"]):
            suggestion["suggestions"][0]["suggestion"]
            if suggestion["token"] in tweet:
                tweet = tweet.replace(suggestion["token"], suggestion["suggestions"][0]["suggestion"])
        return tweet


    # Dicionario com alguns acronimos da lingua inglesa.
    def dictionaryList(self, tweet):
        dictionary = {
            '2F4U': "too fast for you",
            '4YEO': "for your eyes only",
            'FYE': "for your eyes",
            'AAMOF': "as a matter of fact",
            'ACK': "acknowledgment",
            'AFAIK': "as far as i know",
            'AFAIR': "as far as i remember",
            'AFK': "away from keyboard",
            'AKA': "also known as",
            'BTK': "back to keyboard",
            'B2K': "back to keyboard",
            'BTT': "back to topic",
            'BTW': "by the way",
            'BC': "because",
            'CP': "copy and paste",
            'CU': "see you",
            'CYS': "check your settings",
            'DIY': "do it yourself",
            'EOBD': "end of business day",
            'EOM': "end of message",
            'EOT': "end of thread",
            'FAQ': "frequently asked questions",
            'FACK': "full acknowledge",
            'FKA': "formerly known as",
            'FWIW': "for what it's worth",
            'FYI ': "for your information",
            'JFYI': "just for your information",
            'FTW': "fuck the world",
            'HF': "have fun",
            'HTH': "hope this helps",
            'IDK': "i don't know",
            'IIRC': "if i recall correctly",
            'IMHO': "in my humble opinion",
            'IMO': "in my opinion",
            'IMNSHO': "in my not so humbleopinion",
            'IOW': "in other words",
            'ITT': "in this thread",
            'LOL': "laughing out loud",
            'DGMW': "don't get me wrong",
            'MMW': "mark my words",
            'NA': "not available",
            'NAN': "not a number",
            'NNTR': "no need to reply",
            'NOOB ': "newbie",
            'NOYB': "none of your business",
            'NRN': "no reply necessary",
            'OMG': "oh my god",
            'OP': "original poster, original post",
            'OT': "off topic",
            'OTOH': "on the other hand",
            'PEBKAC': "problem exists between keyboard and chai",
            'POV': "point of view",
            'ROTFL': "rolling on the floor laughing",
            'RTFM': "read the fine manual",
            'SCNR': "sorry, could not resist",
            'SFLR': "sorry, for late reply",
            'SPOC': "single point of contact",
            'TBA': "to be announced",
            'TBC': "to be continued",
            'TIA': "thanks in advance",
            'TGIF': "thanks god, its friday",
            'THX': "thanks",
            'TNX': "thanks",
            'TQ': "thank you",
            'TYVM': "thank you very much",
            'TYT': "take your time",
            'TTYL': "talk to you later",
            'WFM': "works for me",
            'WRT': "with regard to",
            'WTH': "what the hell",
            'WTF': "what the fuck",
            'YMMD': "you made my day",
            'YMMV': "your mileage may vary",
            'YAM': "yet another meeting",
            'ICYMI': "in case you missed it",
            '2MORO': "tomorrow",
            '2NTE': "tonight",
            'AEAP': "as early as possible",
            'ALAP': "as late as possible",
            'ASAP': "as soon as possible",
            'ASL': "age / sex / location",
            'B3': "blah, blah, blah",
            'B4YKI': "before you know it",
            'BFF': "best friends, forever",
            'BMY': "between me and you",
            'BRB': "be right back",
            'BRT': "be right there",
            'BTAM': "be that as it may",
            'C-P': "sleepy",
            'CTN': "cannot talk now",
            'CUS': "see you soon",
            'CWOT': "complete waste of time",
            'CYT': "see you tomorrow",
            'E123': "easy as 1, 2, 3",
            'EM': "excuse me",
            'EOD': "end of day",
            'F2F': "face to face",
            'FC': "fingers crossed",
            'FOAF': "friend of a friend",
            'GR8': "great",
            'HAK': "hugs and kisses",
            'IDC': "i don't care",
            'ILU': "i love you",
            'ILY': "i love you",
            'IMU': "i miss you",
            'IRL': "in real life",
            'JK': "just kidding",
            'JC': "just checking",
            'JTLYK': "just to let you know",
            'KFY': "kiss for you",
            'KMN': "kill me now",
            'KPC': "keeping parents clueless",
            'L8R': "later",
            'MOF': "male or female",
            'MTFBWY': "may the force be with you",
            'MYOB': "mind your own business",
            'N-A-Y-L': "in a while",
            'NAZ': "name, address, zip",
            'NC': "no comment",
            'NIMBY': "not in my backyard",
            'NM': "never mind",
            'NP': "no problem",
            'NSFW': "not safe for work",
            'NTIM': "not that it matters",
            'NVM': "never mind",
            'OATUS': "on a totally unrelated subject",
            'OIC': "oh, i see",
            'OMW': "on my way",
            'OTL': "out to lunch",
            'OTP': "on the phone",
            'P911': "parent alert",
            'PAL': "parents are listening",
            'PIR': "parent in room",
            'POS': "parent over shoulder",
            'PROP': "proper respect",
            'PROPS': "proper respect",
            'QT': "cutie",
            'RN': "right now",
            'RU': "are you",
            'SEP': "someone else's problem",
            'SITD': "still in the dark",
            'SMIM': "send me an instant message",
            'TMI': "too much information",
            'UR': "you are",
            'W8': "wait",
            'WB': "welcome back",
            'WYCM': "will you call me",
            'WYWH': "wish you were here",
            "AIN'T": "am not",
            "AINT": "am not",
            "GIMME": "give me",
            "GONNA": "going to",
            "GOTTA": "got a",
            "KINDA": "kind of",
            "LEMME": "let me",
            "WANNA": "want a",
            "WHATCHA": "what are you",
            "YA": "you",
            "AB": "about",
            "ABT": "about",
            "AFAIK": "as far as i know",
            "B4": "before",
            "BFN": "bye for now",
            "BGD": "background",
            "BH": "blockhead",
            "BR": "best regards",
            "BTW": "by the way",
            "CHK": "check",
            "CUL8R": "see you later",
            "DAM": "don't annoy me",
            "DD": "dear daughter",
            "DS": "dear son",
            "DYK": "did you know, do you know",
            "EM/EML": "email",
            "EMA": "email address",
            "F2F": "face to face",
            "FTF": "face to face",
            "FB": "facebook",
            "FF": "follow friday",
            "FML": "fuck my life",
            "FOTD": "find of the day",
            "FTW": "for the win",
            "FWIW": "for what it's worth.",
            "GTS": "guess the song",
            "HAGN": "have a good night",
            "HOTD": "headline of the day",
            "HT": "heard through",
            "HTH": "hope that helps",
            "IC": "i see",
            "ICYMI": "in case you missed it",
            "IDK": "i don't know",
            "IIRC": "if i remember correctly",
            "IMHO": "in my humble opinion.",
            "IRL": "in real life",
            "IWSN": "i want sex now",
            "JK": "just kidding, joke",
            "JSYK": "just so you know",
            "JV": "joint venture",
            "KK": "kewl kewl, or ok, got it",
            "KYSO": "knock your socks off",
            "LHH": "laugh hella hard",
            "LMAO": "laughing my ass off",
            "LMK": "let me know",
            "LO": "little one",
            "LOL": "laugh out loud",
            "MM": "music monday",
            "MIRL": "meet in real life",
            "MRJN": "marijuana",
            "NBD": "no big deal",
            "NCT": "nobody cares, though",
            "NJOY": "enjoy",
            "NSFW": "not safe for work",
            "NTS": "note to self",
            "OOMF": "one of my friends/followers",
            "ORLY": "oh, really",
            "PLMK": "please let me know",
            "QOTD": "quote of the day",
            "RTQ": "read the question",
            "SFW": "safe for work",
            "SMDH": "shaking my damn head, smh, only more so",
            "SMH": "shaking my head",
            "SRS": "serious",
            "TFTF": "thanks for the follow",
            "TFTT": "thanks for this tweet",
            "TJ": "tweetjack, or joining a conversation belatedly to contribute to a tangent",
            "TL": "timeline",
            "TLDR": "too long, didn't read",
            "TMB": "tweet me back",
            "TT": "trending topic",
            "TY": "thank you",
            "TYIA": "thank you in advance",
            "TYT": "take your time",
            "TYVW": "thank you very much",
            "WTV": "whatever",
            "YGTR": "you got that right",
            "YKWIM": "you know what i mean",
            "YKYAT": "you know you're addicted to",
            "YMMV": "your mileage may vary",
            "YOLO": "you only live once",
            "YOYO": "you're on your own",
            "YW": "you're welcome"
        }
        possibleAcronym = tweet.upper()
        pattern = re.compile(r'\b(' + '|'.join(dictionary.keys()) + r')\b')
        tweet = pattern.sub(lambda x: dictionary[x.group()], possibleAcronym).lower()
        return tweet

    def processTweet(self, tweet):
        tweet = self.dictionaryList(tweet)
        tweet = self.azureSpellCheck(tweet)
        return tweet
