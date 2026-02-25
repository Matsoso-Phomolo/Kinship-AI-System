from flask import Flask, render_template, request
from pyswip import Prolog
import os

app = Flask(__name__, template_folder="templates")  # Ensure Flask knows where templates are

# Load Prolog knowledge base
prolog = Prolog()
prolog.consult("familytree.pl")


def extract_name(question):
    words = question.lower().split()
    return words[-1].replace("?", "")


def process_question(question):
    question = question.lower()

    relationships = {
        "father of": ("father_of", "father", "Ntate"),
        "mother of": ("mother_of", "mother", "Mme"),
        "brother of": ("brother_of", "brother", ""),
        "sister of": ("sister_of", "sister", ""),
        "grandfather of": ("grandfather_of", "grandfather", ""),
        "grandmother of": ("grandmother_of", "grandmother", ""),
        "aunt of": ("aunt_of", "aunt", ""),
        "uncle of": ("uncle_of", "uncle", ""),
        "ancestor of": ("ancestor_of", "ancestor", "")
    }

    for phrase, (predicate, label, title) in relationships.items():
        if phrase in question:
            person = extract_name(question).capitalize()
            query = f"{predicate}(X, {person})"
            result = list(prolog.query(query))

            if result:
                # Remove duplicates and sort
                answers = sorted({r["X"].capitalize() for r in result})

                if label in ["father", "mother"]:
                    # Only take the first (there should be only one)
                    answer_text = f"{title} {answers[0]} is {person}'s {label}."
                else:
                    answer_text = f"{', '.join(answers)} is {person}'s {label}."

                return answer_text
            else:
                return f"No {label} found for {person}."

    return "Sorry, I don't understand the question."


@app.route("/", methods=["GET", "POST"])
def index():
    answer = ""
    if request.method == "POST":
        question = request.form.get("question")
        if question:
            answer = process_question(question)
    return render_template("index.html", answer=answer)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use Render's assigned port if available
    app.run(host="0.0.0.0", port=port)
