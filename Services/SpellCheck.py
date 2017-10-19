import language_check
import re
from nltk.tokenize import WhitespaceTokenizer

#Corrige erros gramaticais
def grammarCheck(tweet):
    tool = language_check.LanguageTool('en-US')
    matches = tool.check(tweet)
    while (len(matches) != 0):
        tweetLog = tweet
        tweet = language_check.correct(tweet, matches)
        matches = tool.check(tweet)
        if tweet == tweetLog:
            break
    return tweet

#Converte Tokens em uma string.
def untokenize(tokens):
    #text = "".join([" " + i if not i.startswith("'") and i not in string.punctuation else i for i in tokens]).strip()

    text = ' '.join(tokens)
    step1 = text.replace("`` ", '"').replace(" ''", '"').replace('. . .', '...')
    step2 = step1.replace(" ( ", " (").replace(" ) ", ") ")
    step3 = re.sub(r' ([.,:;?!%]+)([ \'"`])', r"\1\2", step2)
    step4 = re.sub(r' ([.,:;?!%]+)$', r"\1", step3)
    step5 = step4.replace(" '", "'").replace(" n't", "n't").replace("can not", "cannot")
    step6 = step5.replace(" ` ", " '")
    text = step6.strip()
    return text

#Dicionario com alguns acronimos da lingua inglesa.
def dictionaryList(token):
    Dictionary = {
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
        'B/C': "because",
        'C&P': "copy and paste",
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
        'N/A': "not available",
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
        'BM&Y': "between me and you",
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
        'J/K': "just kidding",
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
        'PAW': "parents are watching",
        'PIR': "parent in room",
        'POS': "parent over shoulder",
        'PROP': "proper respect",
        'PROPS': "proper respect",
        'QT': "cutie",
        'RN': "right now",
        'RU': "are you",
        'SEP': "someone else's problem",
        'SITD': "still in the dark",
        'SLAP': "sounds like a plan",
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
        "YA": "you"
    }
    possibleAcronym = token.upper()
    token = Dictionary.get(possibleAcronym, token)
    return token

def dictonaryCheck(tweet):
    # TODO-> Adicionar mais versatilidade ao dicionário para palavras junto de símbolos.
    #Possivel solução para alterar tweets em que o ultimo token precise passar pelo dicionário.
    if tweet[len(tweet)-1] == '.':
        tweet.replace(tweet[len(tweet)-1],' .')
    # Separa as palavras do tweet em tokens para analise individual
    tokens = WhitespaceTokenizer().tokenize(tweet)
    tokenCounter=-1
    for token in tokens:
        tokenCounter += 1;
        tokens[tokenCounter] = dictionaryList(token)
    #untokenize() e um metodo criado para converter tokens em uma unica string.
    tweet = untokenize(tokens)
    return tweet

def processTweet(tweet):
    tweet = dictonaryCheck(tweet)
    tweet = grammarCheck(tweet)
    return tweet



