
import json
import os
import re
from openai import OpenAI
from graph_retriever import load_graph, find_related_schemes

DATA_FILE = "schemes.json"
MODEL = "gpt-4.1-mini"
TOP_K = 5

# Possible data-quality issues that need manual checking.
REVIEW_KEYWORDS = [
    "industrial estate",
    "stamp duty",
    "micro and small enterprises",
    "manufacturing sector",
    "government purchases",
    "farm production system",
    "term loan",
    "power tariff",
    "micro nutrient",
    "mortgaged",
    "thrust sector",
    "technology development fund",
    "price preference",
]

def normalize(text):
    return re.findall(r"[a-z0-9]+", str(text).lower())

def needs_review(scheme):
    title = scheme.get("scheme_name", "").lower()
    department = scheme.get("department", "").lower()

    # Flag suspicious combinations for manual review.
    title_matches = any(word in title for word in REVIEW_KEYWORDS)
    department_may_be_inconsistent = (
        "agriculture" in department
        and any(word in title for word in [
            "industrial", "enterprise", "manufacturing",
            "stamp duty", "technology development"
        ])
    )

    return title_matches or department_may_be_inconsistent

def load_schemes():
    if not os.path.exists(DATA_FILE):
        raise FileNotFoundError(
            f"Cannot find {DATA_FILE}. Run this program "
            "from your Knowledge Graph project folder."
        )

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, list):
        raise ValueError("Expected schemes.json to contain a list.")

    return data

def retrieve_schemes(question, schemes):
    question_words = set(normalize(question))
    stop_words = {
        "what", "which", "who", "where", "when", "how",
        "can", "i", "the", "a", "an", "is", "are", "for",
        "to", "of", "and", "in", "do", "does", "about",
        "tell", "me", "please", "scheme", "schemes"
    }
    question_words -= stop_words

    results = []

    for scheme in schemes:
        searchable_fields = [
            "scheme_name",
            "department",
            "district",
            "funding_pattern",
            "beneficiaries",
            "benefits",
            "eligibility",
            "how_to_apply",
            "description",
        ]

        combined_text = " ".join(
            str(scheme.get(field, ""))
            for field in searchable_fields
        )
        scheme_words = set(normalize(combined_text))

        score = len(question_words & scheme_words)

        # Give additional weight to matches in the scheme name.
        name_words = set(normalize(scheme.get("scheme_name", "")))
        score += 3 * len(question_words & name_words)

        if score > 0:
            results.append((score, scheme))

    results.sort(key=lambda item: item[0], reverse=True)
    return [scheme for _, scheme in results[:TOP_K]]


def ask_ai(question, retrieved_schemes, client, graph_facts=None):
    context_records = []

    for scheme in retrieved_schemes:
        record = dict(scheme)
        record["needs_manual_review"] = needs_review(scheme)
        context_records.append(record)

    context = json.dumps(
        context_records,
        ensure_ascii=False,
        indent=2
    )

    graph_context = json.dumps(
        graph_facts or [],
        ensure_ascii=False,
        indent=2
    )

    response = client.responses.create(
        model=MODEL,
        instructions=(
            "You are a helpful assistant for Tamil Nadu government schemes. "
            "Answer using only the supplied scheme records and knowledge graph facts. "
            "Use graph facts to identify related departments, beneficiaries, and benefits, "
            "but do not treat them as independently verified information. "
            "Do not invent eligibility rules, amounts, deadlines, or application steps. "
            "If the supplied data does not answer the question, say so. "
            "Mention the scheme name and relevant details. "
            "If needs_manual_review is true, clearly warn that the source record "
            "may contain inconsistent information and should be verified with "
            "the official department. Do not treat the review flag as proof of an error. "
            "If a graph fact has a review status indicating it needs review, "
            "also explain that it requires verification. "
            "Include source URLs for schemes you discuss."
        ),
        input=(
            f"User question:\n{question}\n\n"
            f"Retrieved scheme records (JSON):\n{context}\n\n"
            f"Knowledge graph facts (JSON):\n{graph_context}"
        ),
    )

    return response.output_text
def main():
    try:
        schemes = load_schemes()
        client = OpenAI()  # Reads OPENAI_API_KEY from the environment.
    except Exception as error:
        print(f"Startup error: {error}")
        return

    print("=" * 60)
    print("Tamil Nadu Government Schemes - AI RAG Chatbot")
    print(f"Loaded schemes: {len(schemes)}")
    print("Type 'exit' or 'quit' to stop.")
    print("=" * 60)

    while True:
        question = input("\nAsk a question: ").strip()

        if question.lower() in {"exit", "quit"}:
            print("Chatbot closed.")
            break

        if not question:
            continue

        retrieved = retrieve_schemes(question, schemes)

        graph = load_graph()
        graph_facts = find_related_schemes(question, graph)

        if not retrieved:
            print(
                "\nNo matching schemes were found in the local dataset. "
                "Try a scheme name or a keyword such as 'farmers', "
                "'subsidy', or 'micro enterprises'."
            )
            continue

        print(f"\nRetrieved {len(retrieved)} scheme record(s):")

        for index, scheme in enumerate(retrieved, start=1):
            status = (
                "NEEDS MANUAL REVIEW"
                if needs_review(scheme)
                else "No automatic review flag"
            )
            print(f"{index}. {scheme.get('scheme_name', 'Unknown scheme')}")
            print(f"   Status: {status}")
            print(f"   Source: {scheme.get('source_url', 'Not available')}")

        print("\nAI answer:\n")

        try:
            answer = ask_ai(question, retrieved, client, graph_facts)
            print(answer)
        except Exception as error:
            print(f"API request failed: {error}")
            print(
                "Check your API key, API account access, available credits, "
                "and model access. Do not share your API key."
            )

if __name__ == "__main__":
    main()
