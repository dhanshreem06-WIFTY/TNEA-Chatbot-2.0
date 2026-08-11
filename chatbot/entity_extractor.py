import re


# ---------------------------------------
# COMMUNITY
# ---------------------------------------

COMMUNITIES = [
    "BC",
    "MBC",
    "SC",
    "ST",
    "SCA",
    "BCM",
    "OC"
]


# ---------------------------------------
# BRANCHES
# ---------------------------------------

BRANCHES = {
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
        "artificial intelligence"
    ],

    "ECE": [
        "ece",
        "electronics and communication",
        "electronics and communication engineering"
    ],

    "EEE": [
        "eee",
        "electrical and electronics",
        "electrical and electronics engineering"
    ],

    "MECH": [
        "mech",
        "mechanical",
        "mechanical engineering"
    ],

    "CIVIL": [
        "civil",
        "civil engineering"
    ]
}


# ---------------------------------------
# DISTRICTS
# ---------------------------------------

DISTRICTS = [
    "chennai",
    "coimbatore",
    "madurai",
    "salem",
    "tiruchirappalli",
    "trichy",
    "erode",
    "tiruppur",
    "vellore",
    "thanjavur",
    "tirunelveli",
    "kanchipuram"
]


# ---------------------------------------
# EXTRACT CUTOFF
# ---------------------------------------

def extract_cutoff(text):

    patterns = [

        r"cutoff\s*(?:is|=|:)?\s*(\d+(?:\.\d+)?)",

        r"cut off\s*(?:is|=|:)?\s*(\d+(?:\.\d+)?)",

        r"score\s*(?:is|=|:)?\s*(\d+(?:\.\d+)?)",

        r"(\d{2,3}\.\d+)\s*cutoff",

        r"(\d{2,3})\s*cutoff"

    ]


    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            return float(match.group(1))


    return None


# ---------------------------------------
# EXTRACT COMMUNITY
# ---------------------------------------

def extract_community(text):

    text_upper = text.upper()


    # Check longer/more specific categories first
    communities = [
        "SCA",
        "BCM",
        "MBC",
        "BC",
        "SC",
        "ST",
        "OC"
    ]


    for community in communities:

        pattern = r"\b" + re.escape(community) + r"\b"

        if re.search(pattern, text_upper):

            return community


    return None


# ---------------------------------------
# EXTRACT BRANCH
# ---------------------------------------

def extract_branch(text):

    text_lower = text.lower()


    for branch, names in BRANCHES.items():

        for name in names:

            if name in text_lower:

                return branch


    return None


# ---------------------------------------
# EXTRACT DISTRICT
# ---------------------------------------

def extract_district(text):

    text_lower = text.lower()


    for district in DISTRICTS:

        if district in text_lower:

            return district.title()


    return None


# ---------------------------------------
# EXTRACT ALL ENTITIES
# ---------------------------------------

def extract_entities(text):

    entities = {

        "cutoff": extract_cutoff(text),

        "community": extract_community(text),

        "branch": extract_branch(text),

        "district": extract_district(text)

    }


    return entities


# ---------------------------------------
# TEST
# ---------------------------------------

if __name__ == "__main__":

    question = (
        "My cutoff is 188.5, "
        "I am BC and I want CSE "
        "colleges in Chennai"
    )


    print("Student question:")
    print(question)

    print("\nExtracted entities:")

    entities = extract_entities(question)

    for key, value in entities.items():

        print(f"{key}: {value}")