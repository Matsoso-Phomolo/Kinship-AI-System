from flask import Flask, render_template, request
from pyswip import Prolog
import re

app = Flask(__name__)

# Load PROLOG knowledge base
prolog = Prolog()
prolog.consult("familytree.pl")

# ---------------------------
# Gender → Title
# ---------------------------
def get_title(name):
    name = name.lower()
    if list(prolog.query(f"male({name})")):
        return f"Ntate {name.capitalize()}"
    elif list(prolog.query(f"female({name})")):
        return f"Mme {name.capitalize()}"
    else:
        return name.capitalize()

# ---------------------------
# Relationship Mapping
# ---------------------------
relationships = {
    "father": "father_of",
    "mother": "mother_of",
    "grandfather": "grandfather_of",
    "grandmother": "grandmother_of",
    "brother": "brother_of",
    "sister": "sister_of",
    "uncle": "uncle_of",
    "aunt": "aunt_of",
    "ancestor": "ancestor_of"
}

# ---------------------------
# Format Answer Properly
# ---------------------------
def format_answer(names, person, relation):
    if not names:
        return f"No {relation} found for {person.capitalize()}."

    formatted = [get_title(name) for name in names]

    singular_relations = {"mother", "father", "grandmother", "grandfather"}

    if relation in singular_relations:
        # Only take the first result for singular relations
        return f"{formatted[0]} is {person.capitalize()}'s {relation}."
    else:
        if len(formatted) == 1:
            return f"{formatted[0]} is {person.capitalize()}'s {relation}."
        else:
            names_str = ", ".join(formatted)
            return f"{names_str} are {person.capitalize()}'s {relation}s."

# ---------------------------
# Main NLP Processor
# ---------------------------
def process_question(question):
    question = question.lower().strip()

    # Who is X's Y?
    match = re.search(r"who is (\w+)'s (\w+)", question)
    if match:
        person = match.group(1)
        relation = match.group(2)

        if relation in relationships:
            predicate = relationships[relation]
            # Debug: only for mother/father check
            if relation in {"mother", "father"}:
                results = list(prolog.query(f"{predicate}(X,{person})"))
                print("DEBUG: direct", relation, "query:", results)
            else:
                results = list(prolog.query(f"{predicate}(X,{person})"))

            unique_names = sorted(set(r["X"] for r in results))
            return format_answer(unique_names, person, relation)

    # Who is the Y of X?
    match = re.search(r"who is the (\w+) of (\w+)", question)
    if match:
        relation = match.group(1)
        person = match.group(2)

        if relation in relationships:
            predicate = relationships[relation]
            results = list(prolog.query(f"{predicate}(X,{person})"))
            unique_names = sorted(set(r["X"] for r in results))
            return format_answer(unique_names, person, relation)

    # List all children of X
    match = re.search(r"(list|who are) (all )?children of (\w+)", question)
    if match:
        person = match.group(3)
        results = list(prolog.query(f"parent_of(X,{person})"))
        unique_names = sorted(set(r["X"] for r in results))

        if not unique_names:
            return f"{person.capitalize()} has no children in the knowledge base."

        formatted = [get_title(name) for name in unique_names]

        if len(formatted) == 1:
            return f"{formatted[0]} is the child of {person.capitalize()}."
        else:
            names_str = ", ".join(formatted)
            return f"{names_str} are the children of {person.capitalize()}."

    # Is X a Y of Z?
    match = re.search(r"is (\w+) a (\w+) of (\w+)", question)
    if match:
        person1 = match.group(1)
        relation = match.group(2)
        person2 = match.group(3)

        if relation in relationships:
            predicate = relationships[relation]
            result = list(prolog.query(f"{predicate}({person1},{person2})"))

            if result:
                return f"Yes, {get_title(person1)} is {person2.capitalize()}'s {relation}."
            else:
                return f"No, {get_title(person1)} is not {person2.capitalize()}'s {relation}."

    return "Sorry, I don't understand the question."

# ---------------------------
# Flask Route
# ---------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    answer = ""
    if request.method == "POST":
        question = request.form["question"]
        answer = process_question(question)
    return render_template("index.html", answer=answer)

# ---------------------------
# Run Locally
# ---------------------------
if __name__ == "__main__":
    app.run(debug=True)
