import json
import re


# ---------------------------------------
# LOAD INTENTS
# ---------------------------------------

with open("intents.json", "r", encoding="utf-8") as file:

    intents_data = json.load(file)


# ---------------------------------------
# NORMALIZE TEXT
# ---------------------------------------

def normalize_text(text):

    text = text.lower()

    text = re.sub(r"[^a-z0-9\s]", "", text)

    return text.strip()


# ---------------------------------------
# FIND INTENT
# ---------------------------------------

def detect_intent(user_message):

    user_message = normalize_text(user_message)

    best_intent = "unknown"

    best_score = 0


    for intent in intents_data["intents"]:

        tag = intent["tag"]

        patterns = intent["patterns"]


        for pattern in patterns:

            pattern = normalize_text(pattern)


            # Exact match
            if user_message == pattern:

                return tag


            # Word matching
            user_words = set(user_message.split())

            pattern_words = set(pattern.split())


            common_words = (
                user_words.intersection(pattern_words)
            )


            if len(common_words) > best_score:

                best_score = len(common_words)

                best_intent = tag


    # Require a reasonable match
    if best_score == 0:

        return "unknown"


    return best_intent

if __name__ == "__main__":

    questions = [

        "hello",

        "what is TNEA counselling",

        "show CSE colleges",

        "what is the cutoff",

        "predict my college"

    ]


    for question in questions:

        intent = detect_intent(question)

        print(
            f"Question: {question}"
        )

        print(
            f"Intent: {intent}"
        )

        print("-" * 40)