
import requests
from bs4 import BeautifulSoup

url = "https://www.tn.gov.in/scheme_details.php?id=MTU2Ng=="

headers = {
    "User-Agent": "Mozilla/5.0"
}

try:
    response = requests.get(
        url,
        headers=headers,
        timeout=30
    )

    print("Status Code:", response.status_code)
    print("Final URL:", response.url)
    print("HTML Length:", len(response.text))

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    print("\nPage Title:")
    print(
        soup.title.get_text(strip=True)
        if soup.title else "No title found"
    )

    print("\nHeadings:")
    for heading in soup.find_all(["h1", "h2", "h3"]):
        print(heading.get_text(" ", strip=True))

    print("\nBody Exists:", soup.body is not None)

    print("\nVisible Text Preview:")
    print(soup.get_text(" ", strip=True)[:4000])

    print("\nHTML Preview:")
    print(response.text[:1000])

except requests.RequestException as error:
    print("Request failed:", error)
