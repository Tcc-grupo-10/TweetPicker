from Tweet import Tweet
from TweetPicker.TwitterIntegration import TwitterIntegration


class TweetSearcher(object):
    def __init__(self, run_id, db, interface):
        self.run_id = run_id
        self.db = db
        self.interface = interface
        self.twitter_integration = TwitterIntegration()

    def search_tweets(self, search_key, max_number_of_tweets):

        if search_key != "final paper":
            items = []

            # single words must be searched only as hashtags
            if " " not in search_key:
                if not search_key.startswith("#"):
                    search_key = "#" + search_key

            self.interface.log("Começando captura de Tweets...")
            search_results = self.twitter_integration.getSearch(search_key)
            for status in search_results['statuses']:
                if self.is_not_rt(status["text"]) and (len(items) < max_number_of_tweets):
                    items.append(self.create_tweet(status, search_key))

            self.interface.log("Tweets Capturados: {} tweets".format(len(items)))


            next_url = search_results.get("search_metadata", {}).get("next_results", "")

            while len(items) < max_number_of_tweets:
                search_results = self.twitter_integration.getNextSearch(next_url)
                for status in search_results['statuses']:
                    if self.is_not_rt(status["text"]) and (len(items) < max_number_of_tweets):
                        items.append(self.create_tweet(status, search_key))
                next_url = search_results.get("search_metadata", {}).get("next_results", "")
                self.interface.log("Captured: {} tweets".format(len(items)))

            return items[:max_number_of_tweets]

        else:
            return self.search_tweets_fake()

    def create_tweet(self, status, search_key):
        tweet = Tweet(status, self.run_id, search_key)
        self.db.insert_tweet(tweet)
        return tweet

    def is_not_rt(self, tweet_text):
        return "RT " not in tweet_text

    def search_tweets_fake(self):
        tweets = []

        tweet_texts = [
        "I'll give 20 bucks who could guess what I'm going to reward myself after I'm done with this final paper",
        "Just finish my final paper 😍😍 https://t.co/RBUItXwtKg 🔝",
        "please,  make it stop! i have to finish my final paper study to my finals this week! oh my god",
        "follow everyone who retweets this // 3 mins till the gain tweet // #finalPaper #university",
        "I'm in the process of final final paper I'm not sleeping early 💤",
        "i crammed 4h into 1h because i have the time management skills of a carrot"


        "just got my final paper for a class back and i accidentally submitted the version that shows all revisions and this is the actual most embarrassing moment of my life 😱"
        "test Thursday, presentation Friday, 2 finals Tuesday, 1 final and 1 research paper due Wednesday... *announcer* CAN SHE DO IT?!",
        "Goal tonight: Start and finish final paper; Finish kines project. Will it happen? Probs not 😔",
        "Saturday afternoon. Supporting wife with her final paper. I thought I was done with stuff like that. Apparently, I was wrong...",
        "Working on an outline for my final paper & I have 300+ pages to read....I won’t have any friends until after December 14th lol",
        "When my sister is a tougher professor/grader than my professor (the dean of students)😂 got a 100 on my final paper thanks to him #bless",
        "Just finished my final paper for this class. Four day break between my next one 😩😩",
        "I finished a final paper THREE WEEKS before it’s even due 😎 Who am I !",
        "In case you were wondering: yes, I am writing another final paper on zombies. Yes, I am obsessed. Yes, I may actually be turning into a zombie. 💀",]

        for (n, text) in enumerate(tweet_texts):
            st = self.create_status(text, n)
            tweets.append(Tweet(st, self.run_id, "final paper"))

        return tweets

    def create_status(self, text, id):
        return {
            "text": text,
            "created_at": "",
            "id_str": id
        }
