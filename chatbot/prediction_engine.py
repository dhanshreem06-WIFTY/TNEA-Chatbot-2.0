
import os
import pandas as pd


# ============================================================
# CONFIGURATION
# ============================================================

DATA_FILE = "data/2025 cutoff data.xlsx"

COMMUNITY_COLUMNS = [
    "OC",
    "BC",
    "BCM",
    "MBC",
    "SC",
    "SCA",
    "ST"
]


# ============================================================
# LOAD EXCEL DATASET
# ============================================================

def load_dataset():

    if not os.path.exists(DATA_FILE):
        raise FileNotFoundError(
            f"Dataset not found: {DATA_FILE}"
        )

    # Read Excel without assuming where the header is
    raw_df = pd.read_excel(
        DATA_FILE,
        header=None
    )

    # Find the row containing "Code"
    header_row = None

    for row_number in range(
        min(20, len(raw_df))
    ):

        values = (
            raw_df.iloc[row_number]
            .astype(str)
            .str.strip()
            .str.lower()
            .tolist()
        )

        if "code" in values:
            header_row = row_number
            break

    if header_row is None:
        raise ValueError(
            "Could not find the TNEA header row."
        )

    print(
        f"Header found on Excel row "
        f"{header_row + 1}"
    )

    # Load again using the correct header
    df = pd.read_excel(
        DATA_FILE,
        header=header_row
    )

    # Remove empty rows
    df = df.dropna(how="all")

    # Clean column names
    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
    )

    return df


# ============================================================
# CLEAN CUTOFF
# ============================================================

def clean_cutoff(value):

    if pd.isna(value):
        return None

    value = str(value).strip()

    if value in [
        "",
        "-",
        "—",
        "nan",
        "None"
    ]:
        return None

    try:
        return float(value)

    except (ValueError, TypeError):
        return None


# ============================================================
# NORMALIZE COMMUNITY
# ============================================================

def normalize_community(community):

    if not community:
        return None

    community = str(
        community
    ).upper().strip()

    aliases = {

        "OC": "OC",
        "OPEN": "OC",
        "OPEN CATEGORY": "OC",

        "BC": "BC",
        "BACKWARD CLASS": "BC",

        "BCM": "BCM",
        "BACKWARD CLASS MUSLIM": "BCM",

        "MBC": "MBC",
        "MOST BACKWARD CLASS": "MBC",

        "SC": "SC",
        "SCHEDULED CASTE": "SC",

        "SCA": "SCA",

        "ST": "ST",
        "SCHEDULED TRIBE": "ST"
    }

    return aliases.get(
        community,
        community
    )


# ============================================================
# NORMALIZE BRANCH
# ============================================================

def normalize_branch(branch):

    if not branch:
        return ""

    branch = str(
        branch
    ).lower().strip()

    # CSE
    if (
        branch == "cse"
        or "computer science" in branch
    ):
        return "computer science"

    # AIML
    if (
        branch == "aiml"
        or "artificial intelligence and machine learning" in branch
        or "ai and machine learning" in branch
    ):
        return "artificial intelligence"

    # AI & Data Science
    if (
        branch == "aids"
        or "artificial intelligence and data science" in branch
    ):
        return "artificial intelligence and data science"

    # ECE
    if (
        branch == "ece"
        or "electronics and communication" in branch
    ):
        return "electronics and communication"

    # EEE
    if (
        branch == "eee"
        or "electrical and electronics" in branch
    ):
        return "electrical and electronics"

    # IT
    if (
        branch == "it"
        or "information technology" in branch
    ):
        return "information technology"

    # Mechanical
    if (
        branch == "mech"
        or "mechanical engineering" in branch
    ):
        return "mechanical"

    # Civil
    if (
        branch == "civil"
        or "civil engineering" in branch
    ):
        return "civil"

    # Aeronautical
    if (
        branch == "aero"
        or "aeronautical engineering" in branch
    ):
        return "aeronautical"

    # Automobile
    if (
        branch == "auto"
        or "automobile engineering" in branch
    ):
        return "automobile"

    # Chemical
    if "chemical engineering" in branch:
        return "chemical engineering"

    # Robotics
    if "robotics" in branch:
        return "robotics"

    return branch


# ============================================================
# CHECK BRANCH
# ============================================================

def branch_matches(
    dataset_branch,
    requested_branch
):

    if not requested_branch:
        return True

    dataset_branch = normalize_branch(
        dataset_branch
    )

    requested_branch = normalize_branch(
        requested_branch
    )

    return (
        requested_branch == dataset_branch
        or requested_branch in dataset_branch
    )


# ============================================================
# PREDICT COLLEGES
# ============================================================

def predict_colleges(
    cutoff,
    community,
    branch=None,
    district=None
):

    # --------------------------------------------------------
    # Load dataset
    # --------------------------------------------------------

    try:

        df = load_dataset()

    except Exception as error:

        return {
            "error": str(error)
        }


    # --------------------------------------------------------
    # Check columns
    # --------------------------------------------------------

    required_columns = [
        "Code",
        "College Name",
        "Branch"
    ]

    for column in required_columns:

        if column not in df.columns:

            return {
                "error":
                f"Missing column: {column}"
            }


    # --------------------------------------------------------
    # Community
    # --------------------------------------------------------

    community = normalize_community(
        community
    )

    if community not in COMMUNITY_COLUMNS:

        return {
            "error":
            "Invalid community. "
            "Use OC, BC, BCM, MBC, SC, SCA or ST."
        }


    # --------------------------------------------------------
    # Cutoff
    # --------------------------------------------------------

    try:

        cutoff = float(cutoff)

    except (ValueError, TypeError):

        return {
            "error":
            "Cutoff must be a number."
        }


    # --------------------------------------------------------
    # Check community column
    # --------------------------------------------------------

    if community not in df.columns:

        return {
            "error":
            f"Column {community} not found."
        }


    results = []


    # ========================================================
    # SEARCH DATASET
    # ========================================================

    for _, row in df.iterrows():

        college_name = str(
            row["College Name"]
        ).strip()

        dataset_branch = str(
            row["Branch"]
        ).strip()


        # ----------------------------------------------------
        # Branch filter
        # ----------------------------------------------------

        if branch:

            if not branch_matches(
                dataset_branch,
                branch
            ):
                continue


        # ----------------------------------------------------
        # District filter
        # ----------------------------------------------------

        if district:

            if (
                str(district).lower()
                not in college_name.lower()
            ):
                continue


        # ----------------------------------------------------
        # Historical cutoff
        # ----------------------------------------------------

        historical_cutoff = clean_cutoff(
            row[community]
        )

        if historical_cutoff is None:
            continue


        # ----------------------------------------------------
        # Difference
        # ----------------------------------------------------

        difference = (
            cutoff - historical_cutoff
        )


        # ----------------------------------------------------
        # Prediction category
        # ----------------------------------------------------

        if difference >= 5:

            category = "Strong Possibility"

        elif difference >= 0:

            category = "Possible"

        elif difference >= -3:

            category = "Reach"

        else:

            category = "Unlikely"


        # ----------------------------------------------------
        # Save result
        # ----------------------------------------------------

        results.append({

            "code":
                row["Code"],

            "college":
                college_name,

            "branch":
                dataset_branch,

            "community":
                community,

            "student_cutoff":
                cutoff,

            "historical_cutoff":
                historical_cutoff,

            "difference":
                round(
                    difference,
                    2
                ),

            "category":
                category
        })


    # ========================================================
    # SORT RESULTS
    # ========================================================

    priority = {

        "Strong Possibility": 1,
        "Possible": 2,
        "Reach": 3,
        "Unlikely": 4
    }

    results.sort(
        key=lambda result: (
            priority[
                result["category"]
            ],
            -result[
                "historical_cutoff"
            ]
        )
    )


    return results


# ============================================================
# TEST PROGRAM
# ============================================================

if __name__ == "__main__":

    print()
    print("=" * 60)
    print("       TNEA COLLEGE PREDICTION ENGINE")
    print("=" * 60)
    print()

    print("Loading dataset...")
    print()

    try:

        df = load_dataset()

        print(
            f"Dataset loaded successfully!"
        )

        print(
            f"Rows    : {len(df)}"
        )

        print(
            f"Columns : {len(df.columns)}"
        )

        print()

        print("Columns found:")

        for column in df.columns:

            print(
                f"  {column}"
            )

        print()

    except Exception as error:

        print(
            "ERROR:",
            error
        )

        exit()


    # ========================================================
    # TEST STUDENT
    # ========================================================

    test_cutoff = 188.5
    test_community = "BC"
    test_branch = "CSE"


    print("=" * 60)
    print("TEST STUDENT")
    print("=" * 60)

    print()

    print(
        f"Cutoff    : {test_cutoff}"
    )

    print(
        f"Community : {test_community}"
    )

    print(
        f"Branch    : {test_branch}"
    )

    print()


    # ========================================================
    # RUN PREDICTION
    # ========================================================

    results = predict_colleges(
        cutoff=test_cutoff,
        community=test_community,
        branch=test_branch
    )


    # ========================================================
    # DISPLAY RESULTS
    # ========================================================

    if isinstance(results, dict):

        print(
            "ERROR:",
            results["error"]
        )

    elif len(results) == 0:

        print(
            "No matching colleges found."
        )

    else:

        print(
            f"Found {len(results)} matching options."
        )

        print()

        print("=" * 60)
        print("TOP 20 COLLEGES")
        print("=" * 60)

        print()


        for number, result in enumerate(
            results[:20],
            start=1
        ):

            print(
                f"{number}. "
                f"{result['category']}"
            )

            print(
                f"   College : "
                f"{result['college']}"
            )

            print(
                f"   Branch  : "
                f"{result['branch']}"
            )

            print(
                f"   BC Cutoff: "
                f"{result['historical_cutoff']}"
            )

            print(
                f"   Difference: "
                f"{result['difference']}"
            )

            print()


