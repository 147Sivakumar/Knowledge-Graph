
import json
import time
import re
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.tn.gov.in/"
LIST_URL = "https://www.tn.gov.in/scheme_list.php?dep_id=Mg=="

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; TNGovtSchemesLearningBot/1.0)"
}

session = requests.Session()
session.headers.update(HEADERS)


def get_page(url):
    response = session.get(url, timeout=30)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_field(text, label, next_labels):
    start = text.find(label)

    if start == -1:
        return ""

    start += len(label)
    end = len(text)

    for next_label in next_labels:
        position = text.find(next_label, start)
        if position != -1:
            end = min(end, position)

    return clean_text(text[start:end])


def main():
    print("Fetching scheme list...")

    soup = get_page(LIST_URL)
    schemes = []
    seen_urls = set()

    for link in soup.find_all("a", href=True):
        name = clean_text(link.get_text(" ", strip=True))
        href = link["href"].strip()

        if not name or "scheme_details.php" not in href:
            continue

        detail_url = urljoin(BASE_URL, href)

        if detail_url in seen_urls:
            continue

        seen_urls.add(detail_url)
        print("Extracting:", name)

        try:
            detail_soup = get_page(detail_url)

            # Extract visible text from the webpage.
            page_text = clean_text(detail_soup.get_text(" ", strip=True))

            # Remove common website navigation text.
            marker = "Department Wise Beneficiary wise A to Z Search"
            if marker in page_text:
                page_text = page_text.split(marker, 1)[1]

            labels = [
                "Concerned Department:",
                "Concerned District:",
                "Organisation Name:",
                "Scheme Title/Name:",
                "Associated Scheme:",
                "Sponsered By:",
                "Funding Pattern:",
                "Beneficiaries:",
                "Types of Benefits:",
                "Eligibility criteria:",
                "How To avail:",
                "Validity of the Scheme:",
                "Introduced On:",
                "Description:",
                "Scheme Type:"
            ]

            scheme = {
                "scheme_name": name,
                "department": extract_field(
                    page_text, "Concerned Department:", labels[1:]
                ),
                "district": extract_field(
                    page_text, "Concerned District:", labels[2:]
                ),
                "funding_pattern": extract_field(
                    page_text, "Funding Pattern:", labels[7:]
                ),
                "beneficiaries": extract_field(
                    page_text, "Beneficiaries:", labels[8:]
                ),
                "benefits": extract_field(
                    page_text, "Types of Benefits:", labels[9:]
                ),
                "eligibility": extract_field(
                    page_text, "Eligibility criteria:", labels[10:]
                ),
                "how_to_apply": extract_field(
                    page_text, "How To avail:", labels[11:]
                ),
                "description": extract_field(
                    page_text, "Description:", labels[14:]
                ),
                "source_url": detail_url
            }

            schemes.append(scheme)
            time.sleep(0.3)

        except requests.RequestException as error:
            print(f"Could not fetch {name}: {error}")

    with open("schemes.json", "w", encoding="utf-8") as file:
        json.dump(schemes, file, ensure_ascii=False, indent=2)

    print("\nScraping completed.")
    print("Schemes saved:", len(schemes))
    print("Output file: schemes.json")


if __name__ == "__main__":
    main()
