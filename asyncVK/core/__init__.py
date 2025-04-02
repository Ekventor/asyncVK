import json
from .types import EventParams


VERSION = "5.199"


def get_event_params(event: dict, event_type: str) -> EventParams:
    text = None
    user_id = None
    peer_id = None
    post_id = None
    owner_id = None
    object_id = None
    reply = {}
    action = {}
    payload = {}

    try:
        if event_type == "message_new":
            text = event["object"]["message"]["text"]
            peer_id = event["object"]["message"]["peer_id"]
            user_id = event["object"]["message"]["from_id"]
            object_id = event["object"]["message"]["conversation_message_id"]

            if "reply_message" in event["object"]["message"]:
                reply = {
                    "text": event["object"]["message"]["reply_message"]["text"],
                    "peer_id": event["object"]["message"]["reply_message"]["peer_id"],
                    "user_id": event["object"]["message"]["reply_message"]["from_id"],
                    "object_id": event["object"]["message"]["reply_message"]["conversation_message_id"]
                }

            if "action" in event["object"]["message"]:
                action = {
                    "type": event["object"]["message"]["action"]["type"],
                    "object_id": event["object"]["message"]["action"]["conversation_message_id"],
                    "member_id": event["object"]["message"]["action"]["member_id"],
                    "text": event["object"]["message"]["action"]["message"]
                }

            if "payload" in event["object"]["message"]:
                payload = json.loads(event["object"]["message"]["payload"])

        elif event_type == "message_edit":
            text = event["object"]["text"]
            peer_id = event["object"]["peer_id"]
            user_id = event["object"]["from_id"]
            object_id = event["object"]["conversation_message_id"]

            if "reply_message" in event["object"]:
                reply = {
                    "text": event["object"]["reply_message"]["text"],
                    "peer_id": event["object"]["reply_message"]["peer_id"],
                    "user_id": event["object"]["reply_message"]["from_id"],
                    "object_id": event["object"]["reply_message"]["conversation_message_id"]
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
        "object_id": object_id,
        "reply": reply,
        "action": action,
        "payload": payload
    }
