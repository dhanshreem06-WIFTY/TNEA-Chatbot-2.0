import re
import random

from .intents import INTENTS
from .prediction_engine import predict_colleges


# ============================================================
# EXTRACT CUTOFF
# ============================================================

def extract_cutoff(message):
    """
    Extract a TNEA cutoff between 0 and 200.
    Examples:
        188.5
        195
        176.25
    """

    pattern = r"\b\d{2,3}(?:\.\d+)?\b"

    matches = re.findall(pattern, message)

    for value in matches:
        try:
            number = float(value)

            if 0 <= number <= 200:
                return number

        except ValueError:
            continue

    return None


# ============================================================
# EXTRACT COMMUNITY
# ============================================================

def extract_community(message):

    message = message.upper()

    communities = [
        "BCM",
        "MBC",
        "SCA",
        "SC",
        "ST",
        "BC",
        "OC"
    ]

    for community in communities:

        if re.search(rf"\b{re.escape(community)}\b", message):
            return community

    return None


# ============================================================
# EXTRACT BRANCH
# ============================================================

def extract_branch(message):

    message = message.lower()

    branch_patterns = {

        "CSE": [
            "cse",
            "computer science",
            "computer science engineering"
        ],

        "AIML": [
            "aiml",
            "ai ml",
            "ai and ml",
            "artificial intelligence and machine learning",
            "artificial intelligence & machine learning"
        ],

        "AIDS": [
            "aids",
            "ai ds",
            "ai and data science",
            "artificial intelligence and data science"
        ],

        "ECE": [
            "ece",
            "electronics and communication"
        ],

        "EEE": [
            "eee",
            "electrical and electronics"
        ],

        "IT": [
            "it",
            "information technology"
        ],

        "MECH": [
            "mech",
            "mechanical"
        ],

        "CIVIL": [
            "civil"
        ],

        "AERO": [
            "aero",
            "aeronautical"
        ],

        "AUTOMOBILE": [
            "automobile",
            "auto engineering"
        ],

        "ROBOTICS": [
            "robotics",
            "robotics and automation"
        ]
    }

    for branch, patterns in branch_patterns.items():

        for pattern in patterns:

            # Short abbreviations need whole-word matching.
            if pattern in ["cse", "aiml", "aids", "ece", "eee", "it"]:
                if re.search(rf"\b{re.escape(pattern)}\b", message):
                    return branch

            else:
                if pattern in message:
                    return branch

    return None


# ============================================================
# INTENT DETECTION
# ============================================================

def detect_intent(message):

    message = message.lower().strip()

    best_intent = None
    best_score = 0

    for intent_name, intent_data in INTENTS.items():

        score = 0

        for pattern in intent_data["patterns"]:

            pattern = pattern.lower()

            if pattern in message:
                score += 1

        if score > best_score:
            best_score = score
            best_intent = intent_name

    return best_intent


# ============================================================
# FORMAT PREDICTION RESULTS
# ============================================================

def format_prediction_results(results):

    # Prediction engine returned an error
    if isinstance(results, dict) and "error" in results:

        return (
            "⚠️ I could not complete the college prediction.\n\n"
            f"Reason: {results['error']}"
        )

    # No results
    if not results:

        return (
            "I couldn't find matching colleges in the available "
            "cutoff dataset."
        )

    # If prediction engine returns a DataFrame
    if hasattr(results, "to_dict"):

        results = results.to_dict("records")

    # If prediction engine returns a dictionary containing results
    if isinstance(results, dict):

        if "results" in results:
            results = results["results"]
        else:
            results = [results]

    response = []

    response.append("🎓 TNEA College Prediction")
    response.append("")
    response.append(
        "These predictions are based on the cutoff data available "
        "in the dataset."
    )
    response.append("")

    for index, college in enumerate(results[:20], start=1):

        if isinstance(college, dict):

            college_name = (
                college.get("College Name")
                or college.get("college")
                or college.get("College")
                or "Unknown College"
            )

            branch = (
                college.get("Branch")
                or college.get("branch")
                or "Unknown Branch"
            )

            cutoff = (
                college.get("Cutoff")
                or college.get("cutoff")
                or ""
            )

            if cutoff != "":
                response.append(
                    f"{index}. {college_name}\n"
                    f"   Branch: {branch}\n"
                    f"   Cutoff: {cutoff}"
                )
            else:
                response.append(
                    f"{index}. {college_name}\n"
                    f"   Branch: {branch}"
                )

        else:

            response.append(
                f"{index}. {str(college)}"
            )

    response.append("")
    response.append(
        "⚠️ This is a historical-data-based prediction, "
        "not a guaranteed TNEA allotment."
    )

    return "\n".join(response)


# ============================================================
# MAIN CHAT FUNCTION
# ============================================================

def get_response(message):

    message = message.strip()

    if not message:

        return "Please enter a question."


    # --------------------------------------------------------
    # Extract student information
    # --------------------------------------------------------

    cutoff = extract_cutoff(message)

    community = extract_community(message)

    branch = extract_branch(message)


    # --------------------------------------------------------
    # Detect intent
    # --------------------------------------------------------

    intent = detect_intent(message)


    # --------------------------------------------------------
    # College prediction
    # --------------------------------------------------------

    if (
        intent == "prediction"
        or
        (
            cutoff is not None
            and community is not None
        )
    ):

        if cutoff is None:

            return (
                "📊 I can predict colleges for you.\n\n"
                "Please tell me your cutoff.\n\n"
                "Example:\n"
                "My cutoff is 188.5, I am BC and I want CSE."
            )


        if community is None:

            return (
                "Please tell me your community.\n\n"
                "Available communities:\n"
                "BC, MBC, BCM, SC, SCA, ST or OC."
            )


        results = predict_colleges(
            cutoff=cutoff,
            community=community,
            branch=branch
        )

        return format_prediction_results(results)


    # --------------------------------------------------------
    # Normal intent response
    # --------------------------------------------------------

    if intent in INTENTS:

        responses = INTENTS[intent]["responses"]

        if responses:

            return random.choice(responses)


    # --------------------------------------------------------
    # Default response
    # --------------------------------------------------------

    return (
        "I'm not sure I understood that. 🤔\n\n"
        "You can ask me things like:\n\n"
        "• My cutoff is 188.5, BC, CSE\n"
        "• Which colleges can I get?\n"
        "• What is TNEA counselling?\n"
        "• Explain TNEA cutoff\n"
        "• What branches are available?"
    )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    test_question = (
        "My cutoff is 188.5, I am BC and I want CSE"
    )

    print("\nUSER:")
    print(test_question)

    print("\nBOT:")
    print(get_response(test_question))