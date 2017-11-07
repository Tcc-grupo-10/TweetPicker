class Tweet(object):
    def __init__(self, status, run_id, search_key):

        self.original_tweet = status.get("text", "")
        self.language = status.get("lang", "unknown")
        self.created_at = status.get("created_at")
        self.author_id = status.get("user", {"id_str": "user_not_found"}).get("id_str", "no_id")
        self.number_of_favorites = status.get("favorite_count", 0)
        self.number_of_rts = status.get("retweet_count", 0)
        self.id = status.get("id_str")
        self.search_key = search_key
        self.run_id = run_id

        ######################################
        self.preprocessed_tweet = None
        self.formatted_tweet = None
        self.emojis = []
        self.sentiment = None
        self.is_spam = False
