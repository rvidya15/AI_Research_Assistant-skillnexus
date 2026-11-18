
from ddgs import DDGS

def research_topic(topic):

    print("Agent 1: Searching the web...")

    results = DDGS().text(
        topic,
        max_results=5
    )

    research_data = []

    for i, result in enumerate(results, start=1):

        research_data.append({
            "title": result.get("title", ""),
            "url": result.get("href", ""),
            "body": result.get("body", "")
        })

    if not research_data:
        raise ValueError(
            "No search results found. Try another topic."
        )

    print("Agent 1: Research completed!")

    return research_data