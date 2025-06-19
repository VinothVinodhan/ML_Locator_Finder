# scripts/element_filter.py

from bs4 import BeautifulSoup

def filter_elements_by_action(query_lower: str, soup: BeautifulSoup):
    if "click" in query_lower or "tap" in query_lower:
        return soup.find_all(lambda el: el.name in ["a", "button"])
    if "select" in query_lower or "dropdown" in query_lower:
        return soup.find_all("select")
    if any(w in query_lower for w in ["fill", "enter", "type", "input", "search"]):
        return soup.find_all("input")
    if "check" in query_lower or "checkbox" in query_lower:
        return soup.find_all("input", {"type": "checkbox"})
    if "radio" in query_lower:
        return soup.find_all("input", {"type": "radio"})
    return soup.find_all(["a", "button", "input", "select", "textarea"])
