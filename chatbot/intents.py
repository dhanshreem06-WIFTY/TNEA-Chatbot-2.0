
# ============================================================
# TNEA CHATBOT INTENTS
# ============================================================

INTENTS = {

    "greeting": {
        "patterns": [
            "hi",
            "hello",
            "hey",
            "hi bot",
            "hello bot",
            "good morning",
            "good evening"
        ],
        "responses": [
            "Hello! 👋 I can help you with TNEA counselling, colleges, branches and cutoff predictions.",
            "Hi! 👋 Tell me your TNEA cutoff, community or the college/branch you are interested in."
        ]
    },

    "help": {
        "patterns": [
            "help",
            "what can you do",
            "how can you help",
            "what can i ask",
            "what do you know"
        ],
        "responses": [
            "I can help with TNEA cutoff predictions, college recommendations, branches, communities and counselling information."
        ]
    },

    "prediction": {
        "patterns": [
            "which college can i get",
            "which colleges can i get",
            "what college can i get",
            "what colleges can i get",
            "college prediction",
            "predict my college",
            "predict colleges",
            "college predictor",
            "can i get a college",
            "can i get cse",
            "which college is possible",
            "which college is possible for me",
            "colleges based on my cutoff",
            "college based on cutoff",
            "colleges for my cutoff"
        ],
        "responses": []
    },

    "cutoff": {
        "patterns": [
            "what is cutoff",
            "what is tnea cutoff",
            "how is cutoff calculated",
            "explain cutoff",
            "cutoff meaning",
            "how does cutoff work"
        ],
        "responses": [
            "TNEA engineering cutoff is calculated using your Mathematics, Physics and Chemistry marks. The maximum cutoff is 200."
        ]
    },

    "community": {
        "patterns": [
            "what is bc",
            "what is mbc",
            "what is bcm",
            "what is sc",
            "what is sca",
            "what is st",
            "what is oc",
            "community",
            "community reservation",
            "explain communities"
        ],
        "responses": [
            "TNEA cutoff availability depends on the student's community category. The main categories in our dataset are OC, BC, BCM, MBC, SC, SCA and ST."
        ]
    },

    "counselling": {
        "patterns": [
            "what is tnea counselling",
            "how does tnea counselling work",
            "tnea counselling process",
            "counselling process",
            "how to apply for tnea",
            "tnea admission process"
        ],
        "responses": [
            "TNEA counselling generally involves registration, payment, certificate verification, rank publication, choice filling, tentative allotment and final allotment."
        ]
    },

    "branches": {
        "patterns": [
            "what branches are available",
            "what branches are available?",
            "which branches are available",
            "which branches are available?",
            "what engineering branches are available",
            "which engineering branches are available",
            "what courses are available",
            "which courses are available",
            "what branches can I choose",
            "which branches can I choose",
            "tell me the branches",
            "list the branches",
            "show me the branches",
            "available branches",
            "engineering branches",
            "branches in tnea",
            "branches offered in tnea",
            "what courses does tnea offer"
        ],
        "responses": [
            "TNEA offers many engineering branches such as CSE, ECE, EEE, Mechanical, Civil, IT and more depending on the college and cutoff."
        ]
    },

    "goodbye": {
        "patterns": [
            "bye",
            "goodbye",
            "see you",
            "thanks",
            "thank you"
        ],
        "responses": [
            "You're welcome! All the best for your TNEA counselling! 🎓",
            "Good luck with your college selection! 🎓"
        ]
    }
}

