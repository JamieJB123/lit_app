import json
from typing import Dict
from py2neo import Graph, Node, Relationship

# helper label mapping (prefer nicer labels)
ATTRIBUTE_LABEL_MAP = {
    "genres": "Genre",
    "themes_motifs": "Theme",
    "character_types": "CharacterArchetype",
    "writing_styles": "Style",
    "narrative_structure": "NarrativeStructure",
    "philosophical_outlooks": "Philosophy",
    "social_contexts": "SocialContext",
    "historical_contexts": "HistoricalContext",
    "literary_context": "LiteraryContext",
    "main_locations": "Place",
    "tones": "Tone",
    "moods": "Mood",
    "literary_significance": "Significance",
    "cross_domain_influences": "CrossInfluence",
    "influenced_books": "Influenced",
    "influences_on_book": "InfluencedBy",
}

SINGLE_VAL_LABEL_MAP = {
    "form": "Form",
    "author_nationality": "Nationality",
    "author_period": "AuthorPeriod",
    "time_period": "TimePeriod",
    "geographic_scope": "Scope",
    "critical_reception": "Reception",
    "difficulty_level": "Level"
}

BOOK_ATTRIBUTE_TYPES_SINGLE_VAL = [
    "form",
    "author_nationality",
    "author_period",
    "time_period",
    "geographic_scope",
    "critical_reception",
    "difficulty_level",
]

BOOK_ATTRIBUTE_TYPES = [
    "genres",
    "themes_motifs",
    "character_types",
    "writing_styles",
    "narrative_structure",
    "philosophical_outlooks",
    "social_contexts",
    "historical_contexts",
    "literary_context",
    "main_locations",
    "tones",
    "moods",
    "literary_significance",
    "cross_domain_influences",
    "influenced_books",
    "influences_on_book",
]

graph = Graph("neo4j://127.0.0.1:7687", auth=("neo4j", "12345678"))

def add_book_to_graph(book: Dict):
    book_node = Node("Book", title=book["title"], author=book.get("author"), year=book.get("year"))
    print(book_node)
    graph.merge(book_node, "Book", "title")

    # Multi-valued attributes

    for attribute in BOOK_ATTRIBUTE_TYPES:
        values = book.get(attribute, [])
        label = ATTRIBUTE_LABEL_MAP.get(attribute, attribute.capitalize())

        for value in values:
            name = value
            print(name)

            attribute_node = Node(label, name=name)
            print(attribute_node)
            graph.merge(attribute_node, label, "name")

            rel = Relationship(book_node, f"HAS_{label.upper()}", attribute_node)
            print(rel)
            graph.merge(rel)

    # Single-valued attributes

    for attr in BOOK_ATTRIBUTE_TYPES_SINGLE_VAL:
        value = book.get(attr)
        if value:
            label = SINGLE_VAL_LABEL_MAP.get(attr, attr.capitalize())
            print(value, label)

            attr_node = Node(label, name=value)
            print(attr_node)
            graph.merge(attr_node, label, "name")

            rel_2 = Relationship(book_node, f"HAS_{label.upper()}", attr_node)
            print(rel_2)
            graph.merge(rel_2)

if __name__ == "__main__":
    with open("data/data.json", "r") as f:
        book_data = json.load(f)

    graph.delete_all()

    for book in book_data:
        print(f"{book.get('title')} by {book.get('author')}")
        try:
            add_book_to_graph(book)
        except:
            print(f"Problem with {book.get('title')}")
