from bs4 import BeautifulSoup
from scripts.locator_utils import generate_locator
from scripts.element_filter import filter_elements_by_action

def process_html(query: str, html_content: str):
    soup = BeautifulSoup(html_content, "html.parser")
    query_lower = query.lower()
    filtered_elements = filter_elements_by_action(query, soup)

    best_match = None
    best_score = -1

    # Common stopwords to ignore in scoring
    stopwords = {"to", "the", "a", "an", "of", "in", "on", "at", "for", "and", "or", "is", "site", "link", "button"}
    query_words = [w for w in query_lower.split() if w not in stopwords]
    phrase = " ".join(query_words)

    for element in filtered_elements:
        score = 0
        tag_text = element.get_text(strip=True).lower()

        # 1. Exact phrase match (ignoring stopwords)
        if tag_text == phrase:
            score += 100
        # 2. Phrase contained in element text (as a substring, but not just any substring)
        elif phrase in tag_text and len(phrase.split()) > 1:
            score += 60
        # 3. All query words present as whole words (order doesn't matter)
        elif all(q in tag_text.split() for q in query_words) and len(query_words) > 1:
            score += 30
        # 4. Any query word present as whole word
        elif any(q in tag_text.split() for q in query_words):
            score += 10
        # 5. Partial/substring match (very weak, only if nothing else matches)
        elif any(q in tag_text for q in query_words):
            score += 1

        # Boost if tag matches query intent
        if "link" in query_lower and element.name == "a":
            score += 20
        if "button" in query_lower and element.name == "button":
            score += 20

        # Boost for tag-specific logic
        if element.name in ["button", "input"]:
            score += 3
        if element.name == "select":
            score += 4
        if element.name == "a" and "href" in element.attrs:
            score += 2

        # Match label text for inputs/checkboxes/radios
        if element.name in ["input", "select", "textarea"]:
            label = soup.find("label", attrs={"for": element.get("id", "")})
            if label and any(q in label.get_text(strip=True).lower() for q in query_words):
                score += 4

        # Match sibling label for checkbox/radio
        if element.name == "input" and element.get("type") in ["checkbox", "radio"]:
            label = element.find_next_sibling("label")
            if label and phrase in label.get_text(strip=True).lower():
                score += 4

        if score > best_score:
            best_score = score
            best_match = element

    if best_match:
        locator = generate_locator(best_match)
        print("Found ", locator)
        return {
            "query": query,
            "tag": best_match.name,
            "text": best_match.get_text(strip=True),
            "locator": locator,
            "matching_score": round(best_score / 50, 4)  # normalized score
        }
    else:
        return {"error": "No matching element found"}