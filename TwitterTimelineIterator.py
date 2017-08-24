import Database

def saveNext(searchRaw, rawKey):

    statuses = searchRaw.get("statuses", [])

    for status in statuses:
        item = {
            'tweet_id': status.get("id_str", "123"),
            'text': status.get("text", "tweet not found"),
            'retweet_count': status.get("retweet_count", 0),
            'favorite_count': status.get("favorite_count", 0),
            'user_id': status.get("user", {"id_str": "user_not_found"}).get("id_str", "no_id"),
            'created_at': status.get("created_at", "duno"),
            'language': status.get("lang", "unknown"),
            'search_key': rawKey
        }

        Database.insertItem(item)

    Database.countItens()

    return searchRaw.get("search_metadata", {}).get("next_results", "")