from Databases import Database

tweet15 = Database.getAll(Database.tweetTable)
untweet = Database.getAll(Database.unTweeterizeTable)


def unTweeterizeTableUpdate(tweet_id, clear_text, raw_text):
    Database.unTweeterizeTable.update_item(
        Key={'tweet_id': tweet_id},
        UpdateExpression="set clear_text=:c, raw_text=:r",
        ExpressionAttributeValues={
            ':c': clear_text,
            ':r': raw_text
        },
        ReturnValues="UPDATED_NEW"
    )


removed = 0
updated = 0

for untt in untweet:

    rawTw = filter(lambda x: x["tweet_id"] == untt["tweet_id"], tweet15)

    if len(rawTw) == 1:
        untt["clear_text"] = untt["text"]
        untt["raw_text"] = rawTw[0]["text"]

        if rawTw[0]["search_key"] == "got" and "#got" not in rawTw[0]["text"].lower():
            print ("NOT contains #got " + " | " + rawTw[0]["search_key"] + " | " + rawTw[0]["text"].lower())
            Database.deleteItem(rawTw[0]["tweet_id"], Database.unTweeterizeTable)
            removed = removed + 1
        else:
            print ("UPDATE " + " | " + rawTw[0]["search_key"] + " | " + untt["tweet_id"])
            unTweeterizeTableUpdate(untt["tweet_id"], untt["clear_text"], untt["raw_text"])
            updated = updated + 1

    else:
        print (rawTw)

print ("removed: {}".format(removed))
print ("updated: {}".format(updated))
