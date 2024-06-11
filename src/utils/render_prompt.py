import re


def replace_human_ai(text):
    pattern = r"Human:|AI:"

    replaced_text = re.sub(pattern, lambda match: "Them:" if match.group() == "Human:" else "You:", text)

    return replaced_text
