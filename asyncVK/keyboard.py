import json


class Button:
    def __init__(self, label: str, color: str, payload: dict = ""):
        self.button = {
            "action": {
                "type": "text",
                "label": label,
                "payload": payload
            },
            "color": color
        }

    def __str__(self):
        return json.dumps(self.button)


class Line:
    def __init__(self, *buttons: Button):
        self.line = []
        for button in buttons:
            self.line.append(button.button)

    def __str__(self):
        return json.dumps(self.line)


class Keyboard:
    def __init__(self, *lines: Line, one_time: bool = False, inline: bool = False):
        self.keyboard = {
            "buttons": []
        }

        if inline:
            self.keyboard["inline"] = inline
        else:
            self.keyboard["one_time"] = one_time

        for line in lines:
            self.keyboard["buttons"].append(line.line)

    def __str__(self):
        return json.dumps(self.keyboard)
