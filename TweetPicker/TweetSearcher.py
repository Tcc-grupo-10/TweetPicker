from Tweet import Tweet
from TweetPicker.TwitterIntegration import TwitterIntegration


class TweetSearcher(object):
    def __init__(self, run_id, db, interface):
        self.run_id = run_id
        self.db = db
        self.interface = interface
        self.twitter_integration = TwitterIntegration()

    def search_tweets(self, search_key, max_number_of_tweets):
        items = []

        # single words must be searched only as hashtags
        if " " not in search_key:
            if not search_key.startswith("#"):
                search_key = "#" + search_key

        self.interface.log("Starting tweet capture...")
        search_results = self.twitter_integration.getSearch(search_key)
        for status in search_results['statuses']:
            if self.is_not_rt(status["text"]) and (len(items) < max_number_of_tweets):
                items.append(self.create_tweet(status, search_key))

        self.interface.log("Captured: {} tweets".format(len(items)))


        next_url = search_results.get("search_metadata", {}).get("next_results", "")

        while len(items) < max_number_of_tweets:
            search_results = self.twitter_integration.getNextSearch(next_url)
            for status in search_results['statuses']:
                if self.is_not_rt(status["text"]) and (len(items) < max_number_of_tweets):
                    items.append(self.create_tweet(status, search_key))
            next_url = search_results.get("search_metadata", {}).get("next_results", "")
            self.interface.log("Captured: {} tweets".format(len(items)))

        return items[:max_number_of_tweets]

    def create_tweet(self, status, search_key):
        tweet = Tweet(status, self.run_id, search_key)
        self.db.insert_tweet(tweet)
        return tweet

    def is_not_rt(self, tweet_text):
        return "RT " not in tweet_text
