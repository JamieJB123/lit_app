# improved_books_api.py
from typing import Dict, List, Union, Any
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from py2neo import Graph

# Connect to Neo4j
graph = Graph("bolt://127.0.0.1:7687", auth=("neo4j", "attempt1"))
app = FastAPI()

# ------------- 1) Whitelist mapping -------------
# Map API attribute keys -> actual DB node label and relationship type
ALLOWED_ATTRIBUTES = {
    # api_key: (node_label, relationship_type)
    "genres": ("Genre", "HAS_GENRE"),
    "themes_motifs": ("Theme", "HAS_THEME"),
    "character_types": ("CharacterArchetype", "HAS_CHARACTER"),
    "writing_styles": ("Style", "HAS_STYLE"),
    "narrative_structure": ("NarrativeStructure", "HAS_NARRATIVESTRUCTURE"),
    "philosophical_outlooks": ("Philosophy", "HAS_PHILOSOPHY"),
    "social_contexts": ("SocialContext", "HAS_SOCIALCONTEXT"),
    "historical_contexts": ("HistoricalContext", "HAS_HISTORICALCONTEXT"),
    "literary_context": ("LiteraryContext", "HAS_LITERARYCONTEXT"),
    "main_locations": ("Place", "HAS_PLACE"),
    "tones": ("Tone", "HAS_TONE"),
    "moods": ("Mood", "HAS_MOOD"),
    "literary_significance": ("Significance", "HAS_SIGNIFICANCE"),
    "cross_domain_influences": ("CrossInfluence", "HAS_CROSSINFLUENCE"),
    # add more keys as you support them...
}

# ------------- 2) Request model -------------
# Allow each attribute value to be either a single string or a list of strings
class AttributeRequest(BaseModel):
    attributes: Dict[str, Union[str, List[str]]]

# ------------- 3) Endpoint -------------
@app.post("/books/by_attributes")
def get_books_by_attributes(
    req: AttributeRequest,
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
):
    """
    Example body:
    {
        "attributes": {
            "themes_motifs": ["existentialism", "alienation"],
            "genres": "modernist novel"
        }
    }
    Returns: list of books (title, author, year, internal_id)
    """

    attributes = req.attributes

    # Validate keys: ensure user only provided allowed attribute names
    for k in attributes.keys():
        if k not in ALLOWED_ATTRIBUTES:
            raise HTTPException(status_code=400, detail=f"Unknown attribute: {k}")

    match_clauses = []
    where_clauses = []
    params: Dict[str, Any] = {}

    # Build safe parameterized query pieces
    for i, (api_key, value) in enumerate(attributes.items()):
        node_label, rel_type = ALLOWED_ATTRIBUTES[api_key]
        alias = f"a{i}"           # e.g. a0, a1
        # match pattern: Book -[REL]-> (alias:NodeLabel)
        match_clauses.append(f"(b:Book)-[:{rel_type}]->({alias}:{node_label})")

        # Allow passing either a single string or a list
        if isinstance(value, list):
            params[f"{alias}_names"] = value
            where_clauses.append(f"{alias}.name IN ${alias}_names")
        else:
            params[f"{alias}_name"] = value
            where_clauses.append(f"{alias}.name = ${alias}_name")

    # Compose final query
    match_part = ", ".join(match_clauses) if match_clauses else "(b:Book)"
    where_part = " AND ".join(where_clauses) if where_clauses else ""
    cypher = f"""
    MATCH {match_part}
    {"WHERE " + where_part if where_part else ""}
    RETURN DISTINCT b.title AS title, b.author AS author, b.year AS year, id(b) AS id
    SKIP $offset LIMIT $limit
    """
    # add pagination params
    params["limit"] = limit
    params["offset"] = offset

    # run the query
    results = graph.run(cypher, **params).data()

    # results is a list of dicts: [{"title": "...", "author": "...", "year": 1922, "id": 123}, ...]
    return results
