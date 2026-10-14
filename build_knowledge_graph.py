
import json
import re
import networkx as nx

INPUT_FILE = "schemes.json"
OUTPUT_FILE = "schemes_graph.graphml"

# These keywords flag records for review; they do not prove an error.
REVIEW_KEYWORDS = [
    "industrial",
    "enterprise",
    "micro",
    "small & medium",
    "stamp duty",
    "power tariff",
    "unemployment",
]


def clean_id(value):
    """Create a stable, readable graph node identifier."""
    value = re.sub(r"\s+", " ", str(value or "")).strip()
    return value


def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        schemes = json.load(file)

    graph = nx.DiGraph()

    for index, scheme in enumerate(schemes, start=1):
        name = clean_id(scheme.get("scheme_name"))

        if not name:
            print(f"Skipping record {index}: missing scheme name")
            continue

        scheme_id = f"Scheme:{index}"

        title_lower = name.lower()
        needs_review = any(
            keyword in title_lower
            for keyword in REVIEW_KEYWORDS
        )

        graph.add_node(
            scheme_id,
            node_type="Scheme",
            name=name,
            source_url=scheme.get("source_url", ""),
            review_status=(
                "Needs manual review"
                if needs_review
                else "Not flagged by keyword check"
            ),
        )

        department = clean_id(scheme.get("department"))
        if department:
            department_id = f"Department:{department}"

            graph.add_node(
                department_id,
                node_type="Department",
                name=department,
            )

            graph.add_edge(
                scheme_id,
                department_id,
                relationship="REPORTED_AS_BELONGING_TO",
            )

        beneficiaries = clean_id(scheme.get("beneficiaries"))
        if beneficiaries:
            beneficiary_id = f"Beneficiary:{beneficiaries}"

            graph.add_node(
                beneficiary_id,
                node_type="Beneficiary",
                name=beneficiaries,
            )

            graph.add_edge(
                scheme_id,
                beneficiary_id,
                relationship="LISTS_BENEFICIARY",
            )

        benefits = clean_id(scheme.get("benefits"))
        if benefits:
            benefit_id = f"Benefit:{benefits}"

            graph.add_node(
                benefit_id,
                node_type="Benefit",
                name=benefits,
            )

            graph.add_edge(
                scheme_id,
                benefit_id,
                relationship="REPORTS_BENEFIT",
            )

        if needs_review:
            review_id = f"Review:{index}"

            graph.add_node(
                review_id,
                node_type="DataQualityReview",
                name="Potential title/department mismatch",
            )

            graph.add_edge(
                scheme_id,
                review_id,
                relationship="FLAGGED_FOR_REVIEW",
            )

    nx.write_graphml(graph, OUTPUT_FILE)

    flagged = sum(
        1
        for _, data in graph.nodes(data=True)
        if data.get("node_type") == "DataQualityReview"
    )

    print("Knowledge Graph rebuilt successfully.")
    print("Schemes loaded:", len(schemes))
    print("Graph nodes:", graph.number_of_nodes())
    print("Graph relationships:", graph.number_of_edges())
    print("Schemes flagged for review:", flagged)
    print("Saved to:", OUTPUT_FILE)


if __name__ == "__main__":
    main()
