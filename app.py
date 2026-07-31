from flask import Flask, jsonify, render_template, request
from pyswip import Prolog
import logging
import os
import re
from typing import Any


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
    "spouse": "spouse_of",
    "former spouse": "former_spouse_of",
    "step parent": "step_parent_of",
    "step child": "step_child_of",
    "step father": "step_father_of",
    "step mother": "step_mother_of",
    "older sibling": "older_sibling_of",
    "younger sibling": "younger_sibling_of",
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
    "spouses": "spouse",
    "former spouses": "former spouse",
    "step parents": "step parent",
    "step children": "step child",
    "step fathers": "step father",
    "step mothers": "step mother",
    "older siblings": "older sibling",
    "younger siblings": "younger sibling",
}


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
    ("spouse", "spouse_of"),
    ("former spouse", "former_spouse_of"),
    ("step father", "step_father_of"),
    ("step mother", "step_mother_of"),
    ("step parent", "step_parent_of"),
    ("step child", "step_child_of"),
    ("older sibling", "older_sibling_of"),
    ("younger sibling", "younger_sibling_of"),
    ("ancestor", "ancestor_of"),
    ("descendant", "descendant_of"),
    ("parent", "parent_of"),
    ("child", "child_of"),
    ("sibling", "sibling_of"),
    ("grandparent", "grandparent_of"),
    ("grandchild", "grandchild_of"),
]


GENERIC_RELATIONSHIPS = {
    "parent",
    "child",
    "sibling",
    "grandparent",
    "grandchild",
    "ancestor",
    "descendant",
    "step parent",
    "step child",
}


# =========================================================
# PROLOG HELPERS
# =========================================================

def query_prolog(query: str) -> list[dict[str, Any]]:
    try:
        return list(prolog.query(query))
    except Exception:
        logger.exception("Prolog query failed: %s", query)
        return []


def unique_result_values(
    results: list[dict[str, Any]],
    variable: str,
) -> list[str]:
    values: list[str] = []

    for result in results:
        if variable not in result:
            continue

        value = str(result[variable])

        if value not in values:
            values.append(value)

    return values


# =========================================================
# TEXT NORMALIZATION
# =========================================================

def normalize_question(question: str) -> str:
    if not question:
        return ""

    question = question.strip()
    question = re.sub(r"\s+", " ", question)
    question = question.rstrip("?.! ")

    return question


def normalize_relation(relation: str) -> str | None:
    relation = re.sub(
        r"\s+",
        " ",
        relation.strip().lower(),
    )

    if relation in RELATIONSHIPS:
        return relation

    return PLURAL_RELATIONSHIPS.get(relation)


def normalize_lookup_text(value: str) -> str:
    value = value.strip().lower()

    replacements = {
        "’": "'",
        "‘": "'",
        "`": "'",
        "´": "'",
    }

    for old, new in replacements.items():
        value = value.replace(old, new)

    value = re.sub(r"\s+", " ", value)

    return value


# =========================================================
# PERSON METADATA
# =========================================================

def person_exists(person_id: str) -> bool:
    if not person_id:
        return False

    return bool(
        query_prolog(
            f"person({person_id})"
        )
    )


def get_gender(person_id: str) -> str:
    if query_prolog(f"male({person_id})"):
        return "male"

    if query_prolog(f"female({person_id})"):
        return "female"

    return "unknown"


def get_display_name(person_id: str) -> str:
    results = query_prolog(
        f"display_name({person_id}, Name)"
    )

    if results:
        return str(results[0]["Name"])

    return (
        person_id
        .replace("_", " ")
        .title()
    )


def get_aliases(person_id: str) -> list[str]:
    results = query_prolog(
        f"alias({person_id}, Name)"
    )

    return unique_result_values(
        results,
        "Name",
    )


def get_former_names(person_id: str) -> list[str]:
    results = query_prolog(
        f"former_name({person_id}, Name)"
    )

    return unique_result_values(
        results,
        "Name",
    )


def get_title(person_id: str) -> str:
    display = get_display_name(person_id)
    gender = get_gender(person_id)

    if gender == "male":
        return f"Ntate {display}"

    if gender == "female":
        return f"Mme {display}"

    return display


def get_birth_order(person_id: str) -> int | None:
    results = query_prolog(
        f"birth_order({person_id}, Position)"
    )

    if not results:
        return None

    try:
        return int(results[0]["Position"])
    except (TypeError, ValueError):
        return None


# =========================================================
# PERSON LOOKUP / DUPLICATE-NAME HANDLING
# =========================================================

def get_all_people() -> list[str]:
    results = query_prolog("person(X)")

    return sorted(
        set(
            unique_result_values(
                results,
                "X",
            )
        )
    )


def build_person_search_names(person_id: str) -> list[str]:
    names = [
        get_display_name(person_id),
        *get_aliases(person_id),
        *get_former_names(person_id),
    ]

    normalized = []

    for name in names:
        lookup = normalize_lookup_text(name)

        if lookup not in normalized:
            normalized.append(lookup)

    return normalized


def find_people_by_name(name: str) -> list[str]:
    lookup = normalize_lookup_text(name)

    if not lookup:
        return []

    matches = []

    for person_id in get_all_people():
        search_names = build_person_search_names(
            person_id
        )

        if lookup in search_names:
            matches.append(person_id)

    return matches


def person_context_label(person_id: str) -> str:
    name = get_display_name(person_id)

    mothers = unique_result_values(
        query_prolog(
            f"mother_of(X,{person_id})"
        ),
        "X",
    )

    fathers = unique_result_values(
        query_prolog(
            f"father_of(X,{person_id})"
        ),
        "X",
    )

    context = []

    if mothers:
        context.append(
            "mother: "
            + get_display_name(mothers[0])
        )

    if fathers:
        context.append(
            "father: "
            + get_display_name(fathers[0])
        )

    former_names = get_former_names(
        person_id
    )

    if former_names:
        context.append(
            "formerly "
            + ", ".join(former_names)
        )

    if context:
        return (
            f"{name} ({'; '.join(context)})"
        )

    return name


def resolve_person_name(
    raw_name: str,
) -> tuple[str | None, str | None]:
    matches = find_people_by_name(
        raw_name
    )

    if not matches:
        return (
            None,
            f"{raw_name.strip()} is not recorded "
            "in the current family knowledge base.",
        )

    if len(matches) > 1:
        options = [
            person_context_label(person_id)
            for person_id in matches
        ]

        return (
            None,
            "More than one person is named "
            f"{raw_name.strip()}. Please distinguish between: "
            + "; ".join(options)
            + ".",
        )

    return matches[0], None


# =========================================================
# FORMATTING
# =========================================================

def join_names(names: list[str]) -> str:
    if not names:
        return ""

    if len(names) == 1:
        return names[0]

    if len(names) == 2:
        return f"{names[0]} and {names[1]}"

    return (
        ", ".join(names[:-1])
        + f", and {names[-1]}"
    )


def pluralize_relationship(
    relation: str,
    count: int,
) -> str:
    if count == 1:
        return relation

    special = {
        "child": "children",
        "person": "people",
        "former spouse": "former spouses",
        "step child": "step children",
        "step parent": "step parents",
        "older sibling": "older siblings",
        "younger sibling": "younger siblings",
    }

    if relation in special:
        return special[relation]

    if relation.endswith("y"):
        return relation[:-1] + "ies"

    return relation + "s"


def format_relationship_answer(
    people: list[str],
    target_person: str,
    relation: str,
) -> str:
    target_name = get_title(
        target_person
    )

    if not people:
        return (
            f"No {relation} relationship was found "
            f"for {target_name} in the current "
            "knowledge base."
        )

    formatted = [
        get_title(person_id)
        for person_id in people
    ]

    if len(formatted) == 1:
        return (
            f"{formatted[0]} is "
            f"{target_name}'s {relation}."
        )

    relation_plural = pluralize_relationship(
        relation,
        len(formatted),
    )

    return (
        f"{join_names(formatted)} are "
        f"{target_name}'s {relation_plural}."
    )


# =========================================================
# RELATIONSHIP LOOKUP
# =========================================================

def find_relationship(
    relation: str,
    person_name: str,
) -> str:
    relation = normalize_relation(
        relation
    )

    if not relation:
        return (
            "That relationship is not currently supported."
        )

    person_id, error = resolve_person_name(
        person_name
    )

    if error:
        return error

    predicate = RELATIONSHIPS[
        relation
    ]

    results = query_prolog(
        f"{predicate}(X,{person_id})"
    )

    people = unique_result_values(
        results,
        "X",
    )

    return format_relationship_answer(
        people,
        person_id,
        relation,
    )


# =========================================================
# YES / NO VERIFICATION
# =========================================================

def verify_relationship(
    person1_name: str,
    relation: str,
    person2_name: str,
) -> str:
    relation = normalize_relation(
        relation
    )

    if not relation:
        return (
            "That relationship is not currently supported."
        )

    person1, error1 = resolve_person_name(
        person1_name
    )

    if error1:
        return error1

    person2, error2 = resolve_person_name(
        person2_name
    )

    if error2:
        return error2

    predicate = RELATIONSHIPS[
        relation
    ]

    result = query_prolog(
        f"{predicate}({person1},{person2})"
    )

    if result:
        return (
            f"Yes. {get_title(person1)} is "
            f"{get_title(person2)}'s "
            f"{relation}."
        )

    return (
        f"No. {get_title(person1)} is not "
        f"{get_title(person2)}'s "
        f"{relation} according to the "
        "current knowledge base."
    )


# =========================================================
# RELATIONSHIP DISCOVERY
# =========================================================

def discover_relationship(
    person1_name: str,
    person2_name: str,
) -> str:
    person1, error1 = resolve_person_name(
        person1_name
    )

    if error1:
        return error1

    person2, error2 = resolve_person_name(
        person2_name
    )

    if error2:
        return error2

    if person1 == person2:
        return (
            f"{get_title(person1)} refers "
            "to the same person."
        )

    discovered = []

    for relation, predicate in (
        RELATIONSHIP_DISCOVERY_ORDER
    ):
        result = query_prolog(
            f"{predicate}({person1},{person2})"
        )

        if result:
            discovered.append(relation)

    if not discovered:
        return (
            f"No supported relationship between "
            f"{get_title(person1)} and "
            f"{get_title(person2)} could be proven "
            "from the current knowledge base."
        )

    # Remove generic relationships when a more specific
    # relationship is already known.
    specificity = {
        "parent": {"father", "mother"},
        "child": {"son", "daughter"},
        "sibling": {
            "brother",
            "sister",
            "older sibling",
            "younger sibling",
        },
        "grandparent": {
            "grandfather",
            "grandmother",
        },
        "grandchild": {
            "grandson",
            "granddaughter",
        },
        "step parent": {
            "step father",
            "step mother",
        },
    }

    filtered = []

    for relation in discovered:
        specific_options = specificity.get(
            relation
        )

        if specific_options and any(
            option in discovered
            for option in specific_options
        ):
            continue

        filtered.append(relation)

    # Ancestor/descendant are valid but less useful if
    # a direct relationship was found.
    if any(
        relation not in {
            "ancestor",
            "descendant",
        }
        for relation in filtered
    ):
        filtered = [
            relation
            for relation in filtered
            if relation not in {
                "ancestor",
                "descendant",
            }
        ]

    if len(filtered) == 1:
        return (
            f"{get_title(person1)} is "
            f"{get_title(person2)}'s "
            f"{filtered[0]}."
        )

    return (
        f"{get_title(person1)} is related to "
        f"{get_title(person2)} as: "
        f"{join_names(filtered)}."
    )


# =========================================================
# PERSON PROFILE
# =========================================================

def build_person_profile(
    person_id: str,
) -> dict[str, Any]:
    return {
        "id": person_id,
        "name": get_display_name(
            person_id
        ),
        "title": get_title(
            person_id
        ),
        "gender": get_gender(
            person_id
        ),
        "aliases": get_aliases(
            person_id
        ),
        "former_names": get_former_names(
            person_id
        ),
        "birth_order": get_birth_order(
            person_id
        ),
    }


# =========================================================
# NLP PARSER
# =========================================================

NAME_PATTERN = r"(.+?)"


def process_question(question: str) -> str:
    normalized = normalize_question(
        question
    )

    if not normalized:
        return (
            "Please enter a family relationship question."
        )

    lower = normalized.lower()


    # -----------------------------------------------------
    # How is X related to Y?
    # -----------------------------------------------------

    match = re.fullmatch(
        rf"how is {NAME_PATTERN} related to {NAME_PATTERN}",
        lower,
        re.IGNORECASE,
    )

    if match:
        return discover_relationship(
            match.group(1),
            match.group(2),
        )


    # -----------------------------------------------------
    # What is the relationship between X and Y?
    # -----------------------------------------------------

    match = re.fullmatch(
        rf"what is the relationship between "
        rf"{NAME_PATTERN} and {NAME_PATTERN}",
        lower,
        re.IGNORECASE,
    )

    if match:
        return discover_relationship(
            match.group(1),
            match.group(2),
        )


    # -----------------------------------------------------
    # Who is X's relationship?
    #
    # Example:
    # Who is Phomolo Matsoso's mother?
    # -----------------------------------------------------

    match = re.fullmatch(
        rf"who is {NAME_PATTERN}'s "
        rf"([a-z ]+)",
        lower,
        re.IGNORECASE,
    )

    if match:
        person = match.group(1)
        relation = match.group(2)

        normalized_relation = normalize_relation(
            relation
        )

        if normalized_relation:
            return find_relationship(
                normalized_relation,
                person,
            )


    # -----------------------------------------------------
    # Who are X's relationships?
    # -----------------------------------------------------

    match = re.fullmatch(
        rf"who are {NAME_PATTERN}'s "
        rf"([a-z ]+)",
        lower,
        re.IGNORECASE,
    )

    if match:
        person = match.group(1)
        relation = match.group(2)

        normalized_relation = normalize_relation(
            relation
        )

        if normalized_relation:
            return find_relationship(
                normalized_relation,
                person,
            )


    # -----------------------------------------------------
    # Who is the relation of X?
    # -----------------------------------------------------

    match = re.fullmatch(
        rf"who is the ([a-z ]+) of {NAME_PATTERN}",
        lower,
        re.IGNORECASE,
    )

    if match:
        relation = match.group(1)
        person = match.group(2)

        normalized_relation = normalize_relation(
            relation
        )

        if normalized_relation:
            return find_relationship(
                normalized_relation,
                person,
            )


    # -----------------------------------------------------
    # Who are the relations of X?
    # -----------------------------------------------------

    match = re.fullmatch(
        rf"who are the ([a-z ]+) of {NAME_PATTERN}",
        lower,
        re.IGNORECASE,
    )

    if match:
        relation = match.group(1)
        person = match.group(2)

        normalized_relation = normalize_relation(
            relation
        )

        if normalized_relation:
            return find_relationship(
                normalized_relation,
                person,
            )


    # -----------------------------------------------------
    # List relations of X
    # -----------------------------------------------------

    match = re.fullmatch(
        rf"list(?: all)?(?: the)? "
        rf"([a-z ]+) of {NAME_PATTERN}",
        lower,
        re.IGNORECASE,
    )

    if match:
        relation = match.group(1)
        person = match.group(2)

        normalized_relation = normalize_relation(
            relation
        )

        if normalized_relation:
            return find_relationship(
                normalized_relation,
                person,
            )


    # -----------------------------------------------------
    # Is X the/a/an relation of Y?
    # -----------------------------------------------------

    match = re.fullmatch(
        rf"is {NAME_PATTERN} "
        rf"(?:a|an|the) "
        rf"([a-z ]+) of {NAME_PATTERN}",
        lower,
        re.IGNORECASE,
    )

    if match:
        return verify_relationship(
            match.group(1),
            match.group(2),
            match.group(3),
        )


    # -----------------------------------------------------
    # Is X Y's relation?
    # -----------------------------------------------------

    match = re.fullmatch(
        rf"is {NAME_PATTERN} "
        rf"{NAME_PATTERN}'s "
        rf"([a-z ]+)",
        lower,
        re.IGNORECASE,
    )

    if match:
        return verify_relationship(
            match.group(1),
            match.group(3),
            match.group(2),
        )


    # -----------------------------------------------------
    # Who is married to X?
    # -----------------------------------------------------

    match = re.fullmatch(
        rf"who is married to {NAME_PATTERN}",
        lower,
        re.IGNORECASE,
    )

    if match:
        return find_relationship(
            "spouse",
            match.group(1),
        )


    # -----------------------------------------------------
    # Who was married to X?
    # -----------------------------------------------------

    match = re.fullmatch(
        rf"who was married to {NAME_PATTERN}",
        lower,
        re.IGNORECASE,
    )

    if match:
        return find_relationship(
            "former spouse",
            match.group(1),
        )


    return (
        "I could not understand that question yet. "
        "Try questions such as "
        "\"Who is Phomolo Matsoso's mother?\", "
        "\"Who are Phomolo Matsoso's siblings?\", "
        "\"Who is the grandfather of Phomolo Matsoso?\", "
        "\"How is Phomolo Matsoso related to Moleleki Matsoso?\", "
        "\"Who is married to Nkujoana Matsoso?\", or "
        "\"Is Moleleki Matsoso an ancestor of Phomolo Matsoso?\""
    )


# =========================================================
# WEB PAGE ROUTES
# =========================================================

@app.route(
    "/",
    methods=["GET", "POST"],
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
                "Please enter a family relationship question."
            )

        elif len(question) > 300:
            answer = (
                "Your question is too long. "
                "Please use 300 characters or fewer."
            )

        else:
            answer = process_question(
                question
            )

    return render_template(
        "index.html",
        answer=answer,
        question=question,
    )


@app.route(
    "/explorer",
    methods=["GET"],
)
def explorer():
    return render_template(
        "explorer.html"
    )


# =========================================================
# API — PEOPLE
# =========================================================

@app.route(
    "/api/people",
    methods=["GET"],
)
def api_people():
    people = [
        build_person_profile(person_id)
        for person_id in get_all_people()
    ]

    people.sort(
        key=lambda person:
        person["name"].lower()
    )

    return jsonify(
        {
            "count": len(people),
            "people": people,
        }
    )


# =========================================================
# API — PERSON PROFILE
# =========================================================

@app.route(
    "/api/people/<person_id>",
    methods=["GET"],
)
def api_person(person_id: str):
    if not person_exists(
        person_id
    ):
        return jsonify(
            {
                "error": "person_not_found",
                "message": (
                    "That person does not exist "
                    "in the knowledge base."
                ),
            }
        ), 404

    profile = build_person_profile(
        person_id
    )

    return jsonify(profile)


# =========================================================
# API — FAMILY GRAPH
# =========================================================

@app.route(
    "/api/graph",
    methods=["GET"],
)
def api_graph():
    nodes = [
        build_person_profile(person_id)
        for person_id in get_all_people()
    ]

    biological_edges = []

    seen_edges = set()

    for result in query_prolog(
        "graph_edge(Parent,Child)"
    ):
        if (
            "Parent" not in result
            or "Child" not in result
        ):
            continue

        parent = str(
            result["Parent"]
        )

        child = str(
            result["Child"]
        )

        edge_key = (
            "parent",
            parent,
            child,
        )

        if edge_key in seen_edges:
            continue

        seen_edges.add(
            edge_key
        )

        biological_edges.append(
            {
                "source": parent,
                "target": child,
                "relationship": "parent",
                "type": "biological",
            }
        )


    marriage_edges = []

    marriage_seen = set()

    for result in query_prolog(
        "marriage_edge(Person1,Person2)"
    ):
        if (
            "Person1" not in result
            or "Person2" not in result
        ):
            continue

        person1 = str(
            result["Person1"]
        )

        person2 = str(
            result["Person2"]
        )

        unordered = tuple(
            sorted(
                [person1, person2]
            )
        )

        if unordered in marriage_seen:
            continue

        marriage_seen.add(
            unordered
        )

        marriage_edges.append(
            {
                "source": person1,
                "target": person2,
                "relationship": "spouse",
                "type": "marriage",
            }
        )


    step_edges = []

    for result in query_prolog(
        "step_edge(StepParent,StepChild)"
    ):
        if (
            "StepParent" not in result
            or "StepChild" not in result
        ):
            continue

        step_edges.append(
            {
                "source": str(
                    result["StepParent"]
                ),
                "target": str(
                    result["StepChild"]
                ),
                "relationship": "step_parent",
                "type": "step",
            }
        )


    return jsonify(
        {
            "nodes": nodes,
            "edges": biological_edges,
            "marriage_edges": marriage_edges,
            "step_edges": step_edges,
            "node_count": len(nodes),
            "edge_count": len(biological_edges),
            "marriage_edge_count": len(
                marriage_edges
            ),
            "step_edge_count": len(
                step_edges
            ),
        }
    )


# =========================================================
# API — ASK AI
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
                "error": "question_required",
                "message": (
                    "A question is required."
                ),
            }
        ), 400

    if len(question) > 300:
        return jsonify(
            {
                "error": "question_too_long",
                "message": (
                    "Questions are limited "
                    "to 300 characters."
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
            "knowledge_base": (
                "Leloko la Ntate Moleleki Matsoso"
            ),
        }
    )


# =========================================================
# API — RELATIONSHIP DISCOVERY
# =========================================================

@app.route(
    "/api/relationship/<person1>/<person2>",
    methods=["GET"],
)
def api_relationship(
    person1: str,
    person2: str,
):
    if (
        person_exists(person1)
        and person_exists(person2)
    ):
        result = discover_relationship(
            get_display_name(person1),
            get_display_name(person2),
        )

    else:
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
# API — NAME SEARCH
# =========================================================

@app.route(
    "/api/search",
    methods=["GET"],
)
def api_search():
    query = (
        request.args.get(
            "q",
            ""
        )
        .strip()
    )

    if not query:
        return jsonify(
            {
                "count": 0,
                "results": [],
            }
        )

    normalized_query = (
        normalize_lookup_text(
            query
        )
    )

    matches = []

    for person_id in get_all_people():
        search_names = (
            build_person_search_names(
                person_id
            )
        )

        if any(
            normalized_query in name
            for name in search_names
        ):
            matches.append(
                build_person_profile(
                    person_id
                )
            )

    return jsonify(
        {
            "count": len(matches),
            "results": matches,
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
        people = query_prolog(
            "person(X)"
        )

        return jsonify(
            {
                "status": "healthy",
                "service": "Kinship AI",
                "reasoning_engine": "SWI-Prolog",
                "knowledge_base": (
                    "Leloko la Ntate Moleleki Matsoso"
                ),
                "knowledge_base_loaded": bool(
                    people
                ),
                "people_count": len(
                    set(
                        unique_result_values(
                            people,
                            "X",
                        )
                    )
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
        "Unhandled Kinship AI application error."
    )

    return jsonify(
        {
            "error": "internal_server_error",
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
        )
        .lower()
        == "true"
    )

    app.run(
        host="0.0.0.0",
        port=port,
        debug=debug,
)
