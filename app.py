from flask import Flask, jsonify, render_template, request
from pyswip import Prolog
import logging
import os
import re


# =========================================================
# APPLICATION CONFIGURATION
# =========================================================

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

logger = logging.getLogger(__name__)


# =========================================================
# PROLOG KNOWLEDGE BASE
# =========================================================

prolog = Prolog()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KNOWLEDGE_BASE_PATH = os.path.join(BASE_DIR, "familytree.pl")

prolog.consult(KNOWLEDGE_BASE_PATH)


# =========================================================
# RELATIONSHIP DEFINITIONS
# =========================================================

RELATIONSHIPS = {
    "parent": "parent_of",
    "father": "father_of",
    "mother": "mother_of",

    "child": "child_of",
    "son": "son_of",
    "daughter": "daughter_of",

    "sibling": "sibling_of",
    "brother": "brother_of",
    "sister": "sister_of",

    "grandparent": "grandparent_of",
    "grandfather": "grandfather_of",
    "grandmother": "grandmother_of",

    "grandchild": "grandchild_of",
    "grandson": "grandson_of",
    "granddaughter": "granddaughter_of",

    "uncle": "uncle_of",
    "aunt": "aunt_of",

    "niece": "niece_of",
    "nephew": "nephew_of",

    "cousin": "cousin_of",

    "ancestor": "ancestor_of",
    "descendant": "descendant_of",
}


PLURAL_RELATIONSHIPS = {
    "parents": "parent",
    "fathers": "father",
    "mothers": "mother",

    "children": "child",
    "sons": "son",
    "daughters": "daughter",

    "siblings": "sibling",
    "brothers": "brother",
    "sisters": "sister",

    "grandparents": "grandparent",
    "grandfathers": "grandfather",
    "grandmothers": "grandmother",

    "grandchildren": "grandchild",
    "grandsons": "grandson",
    "granddaughters": "granddaughter",

    "uncles": "uncle",
    "aunts": "aunt",

    "nieces": "niece",
    "nephews": "nephew",

    "cousins": "cousin",

    "ancestors": "ancestor",
    "descendants": "descendant",
}


# Relationships where a normal family model usually expects
# a single result.
SINGULAR_RELATIONSHIPS = {
    "father",
    "mother",
}


# Order used by "How is X related to Y?"
#
# More specific relationships should come before generic ones.
RELATIONSHIP_DISCOVERY_ORDER = [
    ("father", "father_of"),
    ("mother", "mother_of"),

    ("son", "son_of"),
    ("daughter", "daughter_of"),

    ("brother", "brother_of"),
    ("sister", "sister_of"),

    ("grandfather", "grandfather_of"),
    ("grandmother", "grandmother_of"),

    ("grandson", "grandson_of"),
    ("granddaughter", "granddaughter_of"),

    ("uncle", "uncle_of"),
    ("aunt", "aunt_of"),

    ("nephew", "nephew_of"),
    ("niece", "niece_of"),

    ("cousin", "cousin_of"),

    ("ancestor", "ancestor_of"),
    ("descendant", "descendant_of"),

    ("parent", "parent_of"),
    ("child", "child_of"),
    ("sibling", "sibling_of"),
    ("grandparent", "grandparent_of"),
    ("grandchild", "grandchild_of"),
]


# =========================================================
# NORMALIZATION
# =========================================================

def normalize_question(question):
    if not question:
        return ""

    question = question.strip()

    question = re.sub(
        r"\s+",
        " ",
        question,
    )

    question = question.rstrip(
        "?.! "
    )

    return question.lower()


def normalize_name(name):
    if not name:
        return None

    name = name.strip().lower()

    # Current Prolog knowledge base uses simple lowercase atoms.
    if not re.fullmatch(r"[a-z]+", name):
        return None

    return name


def normalize_relation(relation):
    if not relation:
        return None

    relation = relation.lower().strip()

    if relation in RELATIONSHIPS:
        return relation

    return PLURAL_RELATIONSHIPS.get(
        relation
    )


def display_name(name):
    return (
        str(name)
        .replace("_", " ")
        .title()
    )


# =========================================================
# PROLOG EXECUTION
# =========================================================

def query_prolog(query):
    try:
        return list(
            prolog.query(query)
        )

    except Exception:
        logger.exception(
            "Prolog query failed: %s",
            query,
        )

        return []


def unique_result_names(
    results,
    variable="X",
):
    names = []

    for result in results:
        if variable not in result:
            continue

        value = str(
            result[variable]
        )

        if value not in names:
            names.append(value)

    return names


def person_exists(name):
    name = normalize_name(name)

    if not name:
        return False

    return bool(
        query_prolog(
            f"person({name})"
        )
    )


# =========================================================
# HUMAN-READABLE NAME FORMATTING
# =========================================================

def get_title(name):
    safe_name = normalize_name(
        str(name)
    )

    if not safe_name:
        return display_name(name)

    if query_prolog(
        f"male({safe_name})"
    ):
        return (
            f"Ntate "
            f"{display_name(safe_name)}"
        )

    if query_prolog(
        f"female({safe_name})"
    ):
        return (
            f"Mme "
            f"{display_name(safe_name)}"
        )

    return display_name(
        safe_name
    )


# =========================================================
# ANSWER HELPERS
# =========================================================

def join_names(names):
    if not names:
        return ""

    if len(names) == 1:
        return names[0]

    if len(names) == 2:
        return (
            f"{names[0]} and "
            f"{names[1]}"
        )

    return (
        ", ".join(names[:-1])
        + f", and {names[-1]}"
    )


def pluralize_relationship(
    relation,
    count,
):
    if count == 1:
        return relation

    special = {
        "child": "children",
        "person": "people",
    }

    if relation in special:
        return special[relation]

    if relation.endswith("y"):
        return (
            relation[:-1]
            + "ies"
        )

    return relation + "s"


def format_relationship_answer(
    names,
    person,
    relation,
):
    person_display = get_title(person)

    if not names:
        return (
            f"No {relation} relationship was found "
            f"for {person_display} in the current "
            f"knowledge base."
        )

    formatted = [
        get_title(name)
        for name in names
    ]

    if (
        relation
        in SINGULAR_RELATIONSHIPS
    ):
        return (
            f"{formatted[0]} is "
            f"{person_display}'s "
            f"{relation}."
        )

    if len(formatted) == 1:
        return (
            f"{formatted[0]} is "
            f"{person_display}'s "
            f"{relation}."
        )

    relation_plural = (
        pluralize_relationship(
            relation,
            len(formatted),
        )
    )

    return (
        f"{join_names(formatted)} are "
        f"{person_display}'s "
        f"{relation_plural}."
    )


# =========================================================
# RELATIONSHIP LOOKUP
# =========================================================

def find_relationship(
    relation,
    person,
):
    relation = normalize_relation(
        relation
    )

    person = normalize_name(
        person
    )

    if not relation:
        return (
            "That relationship is not currently "
            "supported."
        )

    if not person:
        return (
            "That person's name could not "
            "be processed."
        )

    if not person_exists(person):
        return (
            f"{display_name(person)} is not recorded "
            f"in the current family knowledge base."
        )

    predicate = (
        RELATIONSHIPS[
            relation
        ]
    )

    results = query_prolog(
        f"{predicate}(X,{person})"
    )

    names = unique_result_names(
        results
    )

    return (
        format_relationship_answer(
            names,
            person,
            relation,
        )
    )


# =========================================================
# YES / NO RELATIONSHIP CHECK
# =========================================================

def verify_relationship(
    person1,
    relation,
    person2,
):
    person1 = normalize_name(
        person1
    )

    person2 = normalize_name(
        person2
    )

    relation = normalize_relation(
        relation
    )

    if not (
        person1
        and person2
        and relation
    ):
        return (
            "I could not process that "
            "relationship question."
        )

    if not person_exists(person1):
        return (
            f"{display_name(person1)} is not "
            f"recorded in the current "
            f"knowledge base."
        )

    if not person_exists(person2):
        return (
            f"{display_name(person2)} is not "
            f"recorded in the current "
            f"knowledge base."
        )

    predicate = (
        RELATIONSHIPS[
            relation
        ]
    )

    result = query_prolog(
        f"{predicate}"
        f"({person1},{person2})"
    )

    if result:
        return (
            f"Yes. "
            f"{get_title(person1)} is "
            f"{get_title(person2)}'s "
            f"{relation}."
        )

    return (
        f"No. "
        f"{get_title(person1)} is not "
        f"{get_title(person2)}'s "
        f"{relation} according to the "
        f"current knowledge base."
    )


# =========================================================
# RELATIONSHIP DISCOVERY
# =========================================================

def discover_relationship(
    person1,
    person2,
):
    """
    Discover how person1 relates to person2.

    Example:
        How is Jack related to Harry?

    Kinship AI tests relationship predicates in a
    specific order and returns all relationships
    that can be logically proven.
    """

    person1 = normalize_name(
        person1
    )

    person2 = normalize_name(
        person2
    )

    if not person1 or not person2:
        return (
            "I could not process one or both names."
        )

    if person1 == person2:
        return (
            f"{get_title(person1)} and "
            f"{get_title(person2)} refer "
            f"to the same person."
        )

    if not person_exists(person1):
        return (
            f"{display_name(person1)} is not "
            f"recorded in the current "
            f"knowledge base."
        )

    if not person_exists(person2):
        return (
            f"{display_name(person2)} is not "
            f"recorded in the current "
            f"knowledge base."
        )

    discovered = []

    for (
        relationship,
        predicate,
    ) in RELATIONSHIP_DISCOVERY_ORDER:

        result = query_prolog(
            f"{predicate}"
            f"({person1},{person2})"
        )

        if result:
            discovered.append(
                relationship
            )

    if not discovered:
        return (
            f"No supported relationship between "
            f"{get_title(person1)} and "
            f"{get_title(person2)} could be "
            f"proven from the current "
            f"knowledge base."
        )

    # Remove generic relationships when a more
    # descriptive version is available.

    filtering_rules = {
        "parent": {
            "father",
            "mother",
        },

        "child": {
            "son",
            "daughter",
        },

        "sibling": {
            "brother",
            "sister",
        },

        "grandparent": {
            "grandfather",
            "grandmother",
        },

        "grandchild": {
            "grandson",
            "granddaughter",
        },
    }

    final_relationships = []

    for relation in discovered:
        more_specific = (
            filtering_rules.get(
                relation
            )
        )

        if more_specific:
            if any(
                specific
                in discovered
                for specific
                in more_specific
            ):
                continue

        final_relationships.append(
            relation
        )

    # When a direct relationship exists, ancestor /
    # descendant are mathematically true but less useful
    # to the user.

    direct_relationships = {
        "father",
        "mother",
        "son",
        "daughter",
        "brother",
        "sister",
        "grandfather",
        "grandmother",
        "grandson",
        "granddaughter",
        "uncle",
        "aunt",
        "niece",
        "nephew",
        "cousin",
    }

    if any(
        relation
        in direct_relationships
        for relation
        in final_relationships
    ):
        final_relationships = [
            relation
            for relation
            in final_relationships
            if relation
            not in {
                "ancestor",
                "descendant",
            }
        ]

    if len(final_relationships) == 1:
        relation = (
            final_relationships[0]
        )

        return (
            f"{get_title(person1)} is "
            f"{get_title(person2)}'s "
            f"{relation}."
        )

    return (
        f"{get_title(person1)} is related to "
        f"{get_title(person2)} as: "
        f"{join_names(final_relationships)}."
    )


# =========================================================
# QUESTION PROCESSOR
# =========================================================

def process_question(question):
    normalized = (
        normalize_question(
            question
        )
    )

    if not normalized:
        return (
            "Please enter a family "
            "relationship question."
        )


    # =====================================================
    # HOW IS X RELATED TO Y?
    # =====================================================

    match = re.fullmatch(
        r"how is ([a-z]+) related to ([a-z]+)",
        normalized,
    )

    if match:
        return discover_relationship(
            match.group(1),
            match.group(2),
        )


    # =====================================================
    # WHAT IS THE RELATIONSHIP BETWEEN X AND Y?
    # =====================================================

    match = re.fullmatch(
        r"what is the relationship between "
        r"([a-z]+) and ([a-z]+)",
        normalized,
    )

    if match:
        return discover_relationship(
            match.group(1),
            match.group(2),
        )


    # =====================================================
    # WHO IS X'S RELATION?
    #
    # Who is Harry's father?
    # Who is Harry's aunt?
    # =====================================================

    match = re.fullmatch(
        r"who is ([a-z]+)'s ([a-z]+)",
        normalized,
    )

    if match:
        person = match.group(1)
        relation = match.group(2)

        normalized_relation = (
            normalize_relation(
                relation
            )
        )

        if normalized_relation:
            return find_relationship(
                normalized_relation,
                person,
            )


    # =====================================================
    # WHO IS THE RELATION OF X?
    #
    # Who is the father of Harry?
    # =====================================================

    match = re.fullmatch(
        r"who is the ([a-z]+) of ([a-z]+)",
        normalized,
    )

    if match:
        relation = match.group(1)
        person = match.group(2)

        normalized_relation = (
            normalize_relation(
                relation
            )
        )

        if normalized_relation:
            return find_relationship(
                normalized_relation,
                person,
            )


    # =====================================================
    # WHO IS RELATION OF X?
    # =====================================================

    match = re.fullmatch(
        r"who is ([a-z]+) of ([a-z]+)",
        normalized,
    )

    if match:
        relation = match.group(1)
        person = match.group(2)

        normalized_relation = (
            normalize_relation(
                relation
            )
        )

        if normalized_relation:
            return find_relationship(
                normalized_relation,
                person,
            )


    # =====================================================
    # WHO ARE X'S RELATIONS?
    #
    # Who are Harry's ancestors?
    # Who are Harry's grandparents?
    # =====================================================

    match = re.fullmatch(
        r"who are ([a-z]+)'s ([a-z]+)",
        normalized,
    )

    if match:
        person = match.group(1)
        relation = match.group(2)

        normalized_relation = (
            normalize_relation(
                relation
            )
        )

        if normalized_relation:
            return find_relationship(
                normalized_relation,
                person,
            )


    # =====================================================
    # WHO ARE THE RELATIONS OF X?
    #
    # Who are the parents of Harry?
    # Who are the ancestors of Harry?
    # =====================================================

    match = re.fullmatch(
        r"who are the ([a-z]+) of ([a-z]+)",
        normalized,
    )

    if match:
        relation = match.group(1)
        person = match.group(2)

        normalized_relation = (
            normalize_relation(
                relation
            )
        )

        if normalized_relation:
            return find_relationship(
                normalized_relation,
                person,
            )


    # =====================================================
    # LIST RELATIONS OF X
    #
    # List children of Jack
    # List all descendants of Jack
    # List the grandchildren of Jack
    # =====================================================

    match = re.fullmatch(
        r"list(?: all)?(?: the)? "
        r"([a-z]+) of ([a-z]+)",
        normalized,
    )

    if match:
        relation = match.group(1)
        person = match.group(2)

        normalized_relation = (
            normalize_relation(
                relation
            )
        )

        if normalized_relation:
            return find_relationship(
                normalized_relation,
                person,
            )


    # =====================================================
    # IS X A/THE RELATION OF Y?
    #
    # Is Lily the mother of Harry?
    # Is Jack an ancestor of Harry?
    # =====================================================

    match = re.fullmatch(
        r"is ([a-z]+) "
        r"(?:a|an|the) "
        r"([a-z]+) of ([a-z]+)",
        normalized,
    )

    if match:
        return verify_relationship(
            match.group(1),
            match.group(2),
            match.group(3),
        )


    # =====================================================
    # IS X Y'S RELATION?
    #
    # Is Lily Harry's mother?
    # =====================================================

    match = re.fullmatch(
        r"is ([a-z]+) "
        r"([a-z]+)'s "
        r"([a-z]+)",
        normalized,
    )

    if match:
        return verify_relationship(
            match.group(1),
            match.group(3),
            match.group(2),
        )


    # =====================================================
    # FALLBACK
    # =====================================================

    return (
        "I could not understand that question yet. "
        "Try questions such as "
        "\"Who are the parents of Harry?\", "
        "\"Who is Harry's grandmother?\", "
        "\"Who are Jack's descendants?\", "
        "\"Is Lily the mother of Harry?\", or "
        "\"How is Jack related to Harry?\""
    )


# =========================================================
# HOME PAGE
# =========================================================

@app.route(
    "/",
    methods=[
        "GET",
        "POST",
    ],
)
def index():

    answer = ""
    question = ""

    if request.method == "POST":

        question = (
            request.form.get(
                "question",
                "",
            )
            .strip()
        )

        if not question:
            answer = (
                "Please enter a family "
                "relationship question."
            )

        elif len(question) > 250:
            answer = (
                "Your question is too long. "
                "Please use 250 characters "
                "or fewer."
            )

        else:
            answer = (
                process_question(
                    question
                )
            )

    return render_template(
        "index.html",
        answer=answer,
        question=question,
    )


# =========================================================
# API — PEOPLE
# =========================================================

@app.route(
    "/api/people",
    methods=["GET"],
)
def api_people():

    results = query_prolog(
        "person(X)"
    )

    people = unique_result_names(
        results
    )

    people = sorted(
        set(people)
    )

    response = []

    for person in people:

        gender = "unknown"

        if query_prolog(
            f"male({person})"
        ):
            gender = "male"

        elif query_prolog(
            f"female({person})"
        ):
            gender = "female"

        response.append(
            {
                "id": person,
                "name": display_name(
                    person
                ),
                "title": get_title(
                    person
                ),
                "gender": gender,
            }
        )

    return jsonify(
        {
            "count": len(response),
            "people": response,
        }
    )


# =========================================================
# API — ASK
# =========================================================

@app.route(
    "/api/ask",
    methods=["POST"],
)
def api_ask():

    data = (
        request.get_json(
            silent=True
        )
        or {}
    )

    question = str(
        data.get(
            "question",
            ""
        )
    ).strip()

    if not question:
        return jsonify(
            {
                "error": (
                    "question_required"
                ),
                "message": (
                    "A question is required."
                ),
            }
        ), 400

    if len(question) > 250:
        return jsonify(
            {
                "error": (
                    "question_too_long"
                ),
                "message": (
                    "Questions are limited "
                    "to 250 characters."
                ),
            }
        ), 400

    answer = process_question(
        question
    )

    return jsonify(
        {
            "question": question,
            "answer": answer,
            "engine": "SWI-Prolog",
        }
    )


# =========================================================
# API — RELATIONSHIP DISCOVERY
# =========================================================

@app.route(
    "/api/relationship/"
    "<person1>/<person2>",
    methods=["GET"],
)
def api_relationship(
    person1,
    person2,
):

    result = discover_relationship(
        person1,
        person2,
    )

    return jsonify(
        {
            "person1": person1,
            "person2": person2,
            "result": result,
        }
    )


# =========================================================
# HEALTH CHECK
# =========================================================

@app.route(
    "/health",
    methods=["GET"],
)
def health():

    try:
        test_result = query_prolog(
            "person(X)"
        )

        return jsonify(
            {
                "status": "healthy",
                "service": "Kinship AI",
                "reasoning_engine": (
                    "SWI-Prolog"
                ),
                "knowledge_base_loaded": (
                    bool(test_result)
                ),
            }
        ), 200

    except Exception:

        logger.exception(
            "Health check failed."
        )

        return jsonify(
            {
                "status": "unhealthy",
                "service": "Kinship AI",
            }
        ), 503


# =========================================================
# ERROR HANDLERS
# =========================================================

@app.errorhandler(404)
def not_found(error):

    return jsonify(
        {
            "error": "not_found",
            "message": (
                "The requested resource "
                "does not exist."
            ),
        }
    ), 404


@app.errorhandler(500)
def internal_error(error):

    logger.exception(
        "Unhandled Kinship AI error."
    )

    return jsonify(
        {
            "error": (
                "internal_server_error"
            ),
            "message": (
                "Kinship AI could not "
                "complete the request."
            ),
        }
    ), 500


# =========================================================
# LOCAL DEVELOPMENT
# =========================================================

if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            5000,
        )
    )

    debug = (
        os.environ.get(
            "FLASK_DEBUG",
            "false",
        ).lower()
        == "true"
    )

    app.run(
        host="0.0.0.0",
        port=port,
        debug=debug,
)
