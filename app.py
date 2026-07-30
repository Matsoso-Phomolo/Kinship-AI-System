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
# SUPPORTED RELATIONSHIPS
# =========================================================

RELATIONSHIPS = {
    "father": "father_of",
    "mother": "mother_of",
    "grandfather": "grandfather_of",
    "grandmother": "grandmother_of",
    "brother": "brother_of",
    "sister": "sister_of",
    "uncle": "uncle_of",
    "aunt": "aunt_of",
    "ancestor": "ancestor_of",
}


# Relationships that normally produce only one answer.
SINGULAR_RELATIONSHIPS = {
    "father",
    "mother",
}


# =========================================================
# INPUT HELPERS
# =========================================================

def normalize_question(question):
    """
    Normalize the user's natural-language question while
    preserving the meaning required by the parser.
    """

    if not question:
        return ""

    question = question.strip()

    # Collapse repeated whitespace.
    question = re.sub(r"\s+", " ", question)

    # Remove final punctuation that does not affect meaning.
    question = question.rstrip("?.! ")

    return question.lower()


def normalize_name(name):
    """
    Convert a user-supplied name into the safe Prolog atom
    format used by the current familytree.pl knowledge base.

    Current knowledge-base names are simple lowercase atoms:
    jack, helen, james, harry, etc.
    """

    if not name:
        return None

    name = name.strip().lower()

    # Only permit simple alphabetic names for the current
    # knowledge-base format.
    if not re.fullmatch(r"[a-z]+", name):
        return None

    return name


def display_name(name):
    """
    Format a Prolog atom for human-readable output.
    """

    return str(name).replace("_", " ").title()


# =========================================================
# PROLOG HELPERS
# =========================================================

def query_prolog(query):
    """
    Run a Prolog query and return all results.

    Any Prolog failure is logged and converted into an empty
    result so that users do not see an internal server error.
    """

    try:
        return list(prolog.query(query))

    except Exception:
        logger.exception("Prolog query failed: %s", query)
        return []


def get_title(name):
    """
    Add the Sesotho-style title Ntate or Mme when the
    knowledge base contains gender information.
    """

    safe_name = normalize_name(str(name))

    if not safe_name:
        return display_name(name)

    if query_prolog(f"male({safe_name})"):
        return f"Ntate {display_name(safe_name)}"

    if query_prolog(f"female({safe_name})"):
        return f"Mme {display_name(safe_name)}"

    return display_name(safe_name)


def unique_result_names(results, variable="X"):
    """
    Extract unique Prolog result values while keeping output
    predictable.
    """

    names = []

    for result in results:
        if variable not in result:
            continue

        value = str(result[variable])

        if value not in names:
            names.append(value)

    return names


# =========================================================
# ANSWER FORMATTING
# =========================================================

def format_relationship_answer(names, person, relation):
    """
    Convert a set of relationship query results into a
    natural-language response.
    """

    person_display = display_name(person)

    if not names:
        return (
            f"No {relation} relationship was found "
            f"for {person_display} in the current knowledge base."
        )

    formatted_names = [get_title(name) for name in names]

    if relation in SINGULAR_RELATIONSHIPS:
        return (
            f"{formatted_names[0]} is "
            f"{person_display}'s {relation}."
        )

    if len(formatted_names) == 1:
        return (
            f"{formatted_names[0]} is "
            f"{person_display}'s {relation}."
        )

    names_text = ", ".join(formatted_names[:-1])
    names_text += f" and {formatted_names[-1]}"

    return (
        f"{names_text} are "
        f"{person_display}'s {relation}s."
    )


def format_children_answer(names, parent):
    """
    Format children query results.
    """

    parent_display = get_title(parent)

    if not names:
        return (
            f"{parent_display} has no children recorded "
            f"in the current knowledge base."
        )

    children = [get_title(name) for name in names]

    if len(children) == 1:
        return (
            f"{children[0]} is the child of "
            f"{parent_display}."
        )

    children_text = ", ".join(children[:-1])
    children_text += f" and {children[-1]}"

    return (
        f"{children_text} are the children of "
        f"{parent_display}."
    )


# =========================================================
# RELATIONSHIP QUERY
# =========================================================

def find_relationship(relation, person):
    """
    Find all people who have `relation` to `person`.

    Example:
    father_of(X, harry)
    """

    predicate = RELATIONSHIPS.get(relation)

    if not predicate:
        return None

    results = query_prolog(
        f"{predicate}(X,{person})"
    )

    names = unique_result_names(results)

    return format_relationship_answer(
        names,
        person,
        relation,
    )


# =========================================================
# NLP PROCESSOR
# =========================================================

def process_question(question):
    """
    Parse supported natural-language family questions and
    translate them into Prolog queries.
    """

    normalized = normalize_question(question)

    if not normalized:
        return "Please enter a family relationship question."


    # -----------------------------------------------------
    # Pattern:
    # Who is Harry's father?
    # Who is Harry's grandfather?
    # -----------------------------------------------------

    match = re.fullmatch(
        r"who is ([a-z]+)'s ([a-z]+)",
        normalized,
    )

    if match:
        person = normalize_name(match.group(1))
        relation = match.group(2)

        if relation in RELATIONSHIPS and person:
            return find_relationship(
                relation,
                person,
            )


    # -----------------------------------------------------
    # Pattern:
    # Who is the father of Harry?
    # Who is the grandfather of Harry?
    # -----------------------------------------------------

    match = re.fullmatch(
        r"who is the ([a-z]+) of ([a-z]+)",
        normalized,
    )

    if match:
        relation = match.group(1)
        person = normalize_name(match.group(2))

        if relation in RELATIONSHIPS and person:
            return find_relationship(
                relation,
                person,
            )


    # -----------------------------------------------------
    # Pattern:
    # Who is father of Harry?
    #
    # Supports a slightly more conversational variation
    # where "the" is omitted.
    # -----------------------------------------------------

    match = re.fullmatch(
        r"who is ([a-z]+) of ([a-z]+)",
        normalized,
    )

    if match:
        relation = match.group(1)
        person = normalize_name(match.group(2))

        if relation in RELATIONSHIPS and person:
            return find_relationship(
                relation,
                person,
            )


    # -----------------------------------------------------
    # Pattern:
    # Who are Harry's ancestors?
    # Who are Harry's brothers?
    # Who are Harry's sisters?
    # -----------------------------------------------------

    match = re.fullmatch(
        r"who are ([a-z]+)'s ([a-z]+)",
        normalized,
    )

    if match:
        person = normalize_name(match.group(1))
        relation = match.group(2)

        # Convert common plural forms.
        plural_mapping = {
            "ancestors": "ancestor",
            "brothers": "brother",
            "sisters": "sister",
            "uncles": "uncle",
            "aunts": "aunt",
            "grandfathers": "grandfather",
            "grandmothers": "grandmother",
        }

        relation = plural_mapping.get(
            relation,
            relation,
        )

        if relation in RELATIONSHIPS and person:
            return find_relationship(
                relation,
                person,
            )


    # -----------------------------------------------------
    # Pattern:
    # Who are the ancestors of Harry?
    # Who are the brothers of Harry?
    # -----------------------------------------------------

    match = re.fullmatch(
        r"who are the ([a-z]+) of ([a-z]+)",
        normalized,
    )

    if match:
        relation = match.group(1)
        person = normalize_name(match.group(2))

        plural_mapping = {
            "ancestors": "ancestor",
            "brothers": "brother",
            "sisters": "sister",
            "uncles": "uncle",
            "aunts": "aunt",
            "grandfathers": "grandfather",
            "grandmothers": "grandmother",
        }

        relation = plural_mapping.get(
            relation,
            relation,
        )

        if relation in RELATIONSHIPS and person:
            return find_relationship(
                relation,
                person,
            )


    # -----------------------------------------------------
    # Pattern:
    # List children of Lily
    # List all children of Lily
    # Who are the children of Lily
    # Who are all children of Lily
    #
    # parent_of(Parent, Child)
    #
    # Therefore:
    # parent_of(lily, X)
    #
    # finds Lily's children.
    # -----------------------------------------------------

    match = re.fullmatch(
        r"(?:list|who are)(?: all)? "
        r"(?:the )?children of ([a-z]+)",
        normalized,
    )

    if match:
        parent = normalize_name(match.group(1))

        if not parent:
            return "That name cannot be processed."

        results = query_prolog(
            f"parent_of({parent},X)"
        )

        names = unique_result_names(results)

        return format_children_answer(
            names,
            parent,
        )


    # -----------------------------------------------------
    # Pattern:
    # Is Jack the father of Jess?
    # Is Jack a father of Jess?
    # -----------------------------------------------------

    match = re.fullmatch(
        r"is ([a-z]+) (?:a|the) "
        r"([a-z]+) of ([a-z]+)",
        normalized,
    )

    if match:
        person1 = normalize_name(match.group(1))
        relation = match.group(2)
        person2 = normalize_name(match.group(3))

        if (
            person1
            and person2
            and relation in RELATIONSHIPS
        ):
            predicate = RELATIONSHIPS[relation]

            result = query_prolog(
                f"{predicate}({person1},{person2})"
            )

            if result:
                return (
                    f"Yes. {get_title(person1)} is "
                    f"{display_name(person2)}'s "
                    f"{relation}."
                )

            return (
                f"No. {get_title(person1)} is not "
                f"{display_name(person2)}'s "
                f"{relation} according to the "
                f"current knowledge base."
            )


    # -----------------------------------------------------
    # Pattern:
    # Is Jack Jess's father?
    # -----------------------------------------------------

    match = re.fullmatch(
        r"is ([a-z]+) ([a-z]+)'s ([a-z]+)",
        normalized,
    )

    if match:
        person1 = normalize_name(match.group(1))
        person2 = normalize_name(match.group(2))
        relation = match.group(3)

        if (
            person1
            and person2
            and relation in RELATIONSHIPS
        ):
            predicate = RELATIONSHIPS[relation]

            result = query_prolog(
                f"{predicate}({person1},{person2})"
            )

            if result:
                return (
                    f"Yes. {get_title(person1)} is "
                    f"{display_name(person2)}'s "
                    f"{relation}."
                )

            return (
                f"No. {get_title(person1)} is not "
                f"{display_name(person2)}'s "
                f"{relation} according to the "
                f"current knowledge base."
            )


    # -----------------------------------------------------
    # Unsupported question
    # -----------------------------------------------------

    return (
        "I could not understand that question yet. "
        "Try asking something like "
        "\"Who is the father of Harry?\", "
        "\"Who are Harry's ancestors?\", or "
        "\"Is Lily the mother of Harry?\""
    )


# =========================================================
# WEB ROUTES
# =========================================================

@app.route("/", methods=["GET", "POST"])
def index():
    answer = ""
    question = ""

    if request.method == "POST":
        question = request.form.get(
            "question",
            "",
        ).strip()

        if len(question) > 250:
            answer = (
                "Your question is too long. "
                "Please use 250 characters or fewer."
            )

        else:
            answer = process_question(question)

    return render_template(
        "index.html",
        answer=answer,
        question=question,
    )


# =========================================================
# HEALTH CHECK
# =========================================================

@app.route("/health", methods=["GET"])
def health():
    """
    Lightweight health endpoint for Render and operational
    monitoring.
    """

    try:
        # Confirm the Prolog engine can execute a simple query.
        query_prolog("male(jack)")

        return jsonify(
            {
                "status": "healthy",
                "service": "Kinship AI",
                "reasoning_engine": "SWI-Prolog",
            }
        ), 200

    except Exception:
        logger.exception("Health check failed.")

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
            "error": "Not found",
            "message": "The requested resource does not exist.",
        }
    ), 404


@app.errorhandler(500)
def internal_error(error):
    logger.exception(
        "Unhandled Kinship AI application error."
    )

    return jsonify(
        {
            "error": "Internal server error",
            "message": (
                "Kinship AI could not complete the request."
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

    app.run(
        host="0.0.0.0",
        port=port,
        debug=os.environ.get(
            "FLASK_DEBUG",
            "false",
        ).lower() == "true",
        )
