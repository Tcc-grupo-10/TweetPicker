from Databases import Database
from Services import TwitterIntegration


def saveNext(searchRaw, rawKey, runId):

    statuses = searchRaw.get("statuses", [])

    for status in statuses:

        if "RT " not in status["text"]:
            item = {
                'tweet_id': status.get("id_str", "123"),
                'text': status.get("text", "tweet not found"),
                'retweet_count': status.get("retweet_count", 0),
                'favorite_count': status.get("favorite_count", 0),
                'user_id': status.get("user", {"id_str": "user_not_found"}).get("id_str", "no_id"),
                'created_at': status.get("created_at", "duno"),
                'language': status.get("lang", "unknown"),
                'search_key': rawKey,
                'run_id': runId
            }

            Database.insertItem(item, Database.rawTweets)

    return searchRaw.get("search_metadata", {}).get("next_results", "")


def getTweets(tokenUserless, rawKey, tweetAmount, searchEncoded, runId):
    times = tweetAmount / 100 + 1

    searchRaw = TwitterIntegration.getSearch(searchEncoded, tokenUserless)
    nextUrl = saveNext(searchRaw, rawKey, runId)

    for x in range(0, times):
        searchRaw = TwitterIntegration.getNextSearch(nextUrl, tokenUserless)
        nextUrl = saveNext(searchRaw, rawKey, runId)

    return True


"""def waitTime(minutes):
    mins = 0
    while mins != minutes:
        print ">>> Waiting Twitter Rate Limit Reset:", mins, "/", minutes
        time.sleep(60)
        mins += 1


def getTweetsRec(tokenUserless, rawKey, nextUrl, times, runs, searchEncoded):
    print "Run n:", runs
    for x in range(0, times):
        if nextUrl != "":
            searchRaw = TwitterIntegration.getNextSearch(nextUrl, tokenUserless)
            nextUrl = saveNext(searchRaw, rawKey)
        else:
            searchRaw = TwitterIntegration.getSearch(searchEncoded, tokenUserless)
            nextUrl = saveNext(searchRaw, rawKey)

    waitTime(16)
    getTweetsRec(tokenUserless, rawKey, "", times, runs + 1, searchEncoded)"""