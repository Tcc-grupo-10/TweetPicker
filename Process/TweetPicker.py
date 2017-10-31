# from Databases import Database
from Process.Tweet import Tweet
from Services.TwitterIntegration import TwitterIntegration


class TweetPicker(object):

    def __init__(self):
        self.integration = TwitterIntegration()

    def save(self, searchRaw, rawKey, runId):

        statuses = searchRaw.get("statuses", [])

        tweets = []

        for status in statuses:

            if "RT " not in status["text"]:
                tweets.append(Tweet(status.get("text", "tweet not found")))
                item = {
                    'tweet_id': status.get("id_str", "123"),
                    'raw_tweet': status.get("text", "tweet not found"),
                    'retweet_count': status.get("retweet_count", 0),
                    'favorite_count': status.get("favorite_count", 0),
                    'user_id': status.get("user", {"id_str": "user_not_found"}).get("id_str", "no_id"),
                    'created_at': status.get("created_at", "duno"),
                    'language': status.get("lang", "unknown"),
                    'search_key': rawKey,
                    'run_id': runId
                }

                # Database.insertItem(item, Database.rawTweets)
        return tweets

    def getTweets(self, rawKey, tweetAmount, searchEncoded, runId):
        items = []
        count = 100

        if tweetAmount < 100:
            count = tweetAmount

        searchRaw = self.integration.getSearch(searchEncoded, count)
        items.extend(self.save(searchRaw, rawKey, runId))
        nextUrl = searchRaw.get("search_metadata", {}).get("next_results", "")

        while len(items) < tweetAmount:
            searchRaw = self.integration.getNextSearch(nextUrl)
            items.extend(self.save(searchRaw, rawKey, runId))
            nextUrl = searchRaw.get("search_metadata", {}).get("next_results", "")

        return items[:tweetAmount]
