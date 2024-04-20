VERSION = "5.199"


def get_event_params(event: dict, event_type: str) -> dict:
    text = None
    user_id = None
    peer_id = None
    post_id = None
    owner_id = None
    reply_message = {}

    try:
        if event_type == "message_new":
            text = event["object"]["message"]["text"]
            peer_id = event["object"]["message"]["peer_id"]
            user_id = event["object"]["message"]["from_id"]

            if "reply_message" in event["object"]["message"]:
                reply_message = {
                    "text": event["object"]["message"]["reply_message"]["text"],
                    "peer_id": event["object"]["message"]["reply_message"]["peer_id"],
                    "user_id": event["object"]["message"]["reply_message"]["from_id"]
                }

        elif event_type == "message_edit":
            text = event["object"]["text"]
            peer_id = event["object"]["peer_id"]
            user_id = event["object"]["from_id"]

            if "reply_message" in event["object"]:
                reply_message = {
                    "text": event["object"]["reply_message"]["text"],
                    "peer_id": event["object"]["reply_message"]["peer_id"],
                    "user_id": event["object"]["reply_message"]["from_id"]
                }

        elif event_type in ("wall_reply_new", "wall_reply_edit"):
            text = event["object"]["text"]
            owner_id = event["object"]["owner_id"]
            user_id = event["object"]["from_id"]
            post_id = event["object"]["post_id"]

        elif event_type == "wall_post_new":
            text = event["object"]["text"]
            owner_id = event["object"]["owner_id"]
            user_id = event["object"]["from_id"]
            post_id = event["object"]["id"]

        elif event_type in ("board_post_new", "board_post_edit"):
            text = event["object"]["text"]
            owner_id = event["group_id"]
            user_id = event["object"]["from_id"]
            post_id = event["object"]["topic_id"]

    except KeyError:
        pass

    return {
        "type": event_type,
        "text": text,
        "user_id": user_id,
        "peer_id": peer_id,
        "post_id": post_id,
        "owner_id": owner_id,
        "reply_message": reply_message
    }
