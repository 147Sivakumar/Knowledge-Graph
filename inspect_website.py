
import requests
from bs4 import BeautifulSoup

url = "https://www.tn.gov.in/scheme_list.php?dep_id=Mg=="

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
    print("Requested URL:", url)
    print("Final URL:", response.url)

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    print("\nPage Title:")
    print(soup.title.get_text(strip=True) if soup.title else "No title found")

    print("\nPage Text Preview:")
    print(soup.get_text(separator=" ", strip=True)[:2500])

    print("\nLinks containing 'scheme' or 'welfare':")

    for link in soup.find_all("a", href=True):
        text = link.get_text(" ", strip=True)
        href = link["href"]

        if "scheme" in (text + href).lower() or "welfare" in (text + href).lower():
            print(f"{text} -> {href}")

except requests.RequestException as error:
    print("Website request failed:", error)
