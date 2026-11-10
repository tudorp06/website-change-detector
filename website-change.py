import requests
import hashlib
from pathlib import Path
from bs4 import BeautifulSoup
import difflib
from typing import Optional


#method: difflib.unified_diff(a,b) -> creates github-style changelog  between the a and b .

#baseline.write_text(data, encoding="utf-8") -> writes into a file
BASEFILE = Path("baseline.txt", encoding="utf-8")
CONTENTFILE = Path("content.txt", encoding="utf-8")


def hash_content(content: str) -> str:
    # here will go the fetched webpage text, hashed into sha-256s
    content_bytes = content.encode("utf-8")
    content_sha = hashlib.sha256(content_bytes)
    digest = content_sha.hexdigest()

    return digest

def load_baseline() -> Optional[str]:
    if BASEFILE.exists():
        base_text = BASEFILE.read_text(encoding="utf-8")
        return base_text
    return None

def save_baseline(file_content: str) -> None: 
    BASEFILE.write_text(file_content, encoding="utf-8")

def load_content() -> Optional[str]:
     if CONTENTFILE.exists():
            base_content = CONTENTFILE.read_text(encoding="utf-8")
            return base_content
     return None

def save_content(file_content: str) -> None:
    CONTENTFILE.write_text(file_content, encoding="utf-8")

    

def fetch_content(url: str) -> str:

    response = requests.get(url, timeout=15)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    main = soup.select_one("body")
    if main is None:
        raise ValueError("Page has no <main> element")
    main_content = main.get_text(" ", strip=True)
    if not main_content:
      raise ValueError("<main> element has no text.") 
    return main_content

def get_diff(old_content: str, new_content: str) -> str:
    old_lines = old_content.splitlines(keepends=True)
    new_lines = new_content.splitlines(keepends=True)
    diff = " ".join(difflib.unified_diff(old_lines, new_lines))
    return diff


def check_website(url: str) -> None:
    website = fetch_content(url)
    web_digest = hash_content(website)
    base_hash = load_baseline()
    base_content = load_content()
    if base_hash == web_digest:
        print("No change detected on the website.")
    elif base_hash is None:
        save_baseline(web_digest)
        save_content(website)
        print("First run: baseline saved")
    else:
        save_baseline(web_digest)
        save_content(website)
        diff = get_diff("BuildNotch\nPrice: $3\nWindows app\n", "BuildNotch\nPrice: $5\nWindows app\n")
        print("Change detected: ")
        print(diff)




if __name__ == "__main__":
    host_input = input("Please enter the name of the website: ")
    URL = "https://" + host_input
    check_website(URL)  #this is basically a broad implementation where I create the url based on user input, in the MVP it should be one fixed url to track diffs



