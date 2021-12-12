import json


def get_button(label, color, payload=""):
    return {
        "action": {
            "type": "text",
            "payload": json.dumps(payload),
            "label": label
        },
        "color": color
    }


def get_keyboard(buttons, inline=False, one_time=True):
    keyboard = {
        "buttons": [
            [
                get_button(label, color) for label, color in button
            ] for button in buttons
        ]
    }

    if inline:
        keyboard["inline"] = inline
    else:
        keyboard["one_time"] = one_time

    keyboard = json.dumps(keyboard, ensure_ascii=False).encode("UTF-8")
    keyboard = str(keyboard.decode("UTF-8"))

    return keyboard
