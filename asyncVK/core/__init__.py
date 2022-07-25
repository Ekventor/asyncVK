def get_event_params(event: dict, event_type: str) -> dict:
    text = None
    user_id = None
    peer_id = None
    post_id = None
    owner_id = None

    try:
        if event_type == "message_new":
            text = event["object"]["message"]["text"]
            peer_id = event["object"]["message"]["peer_id"]
            user_id = event["object"]["message"]["from_id"]

        elif event_type == "message_edit":
            text = event["object"]["text"]
            peer_id = event["object"]["peer_id"]
            user_id = event["object"]["from_id"]

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
        "owner_id": owner_id
    }
