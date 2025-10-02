from typing import Dict, List, Union, Any
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from py2neo import Graph

graph = Graph("neo4j://127.0.0.1:7687", auth=("neo4j", "12345678"))
app = FastAPI()

class AttributeRequest(BaseModel):
    attributes: Dict[str, Union[str, List[str]]]

@app.post("/books/by_attributes")
def get_books_by_attribute(req: AttributeRequest):

    """
    Expected request body (JSON)
    {
        "attributes": {
            "Genre": ["fantasy", "adventure"],
            "AuthorPeriod": "modern",
            "Theme": ["hero's journey", "coming of age"]
        }
    }
    """

    attributes = req.attributes

    match_clauses = []
    where_clauses = []
    params: Dict[str, Any] = {}

    for i, (attr, value) in enumerate(attributes.items()):
        alias = f"a{i}"
        node_label = attr
        rel_type = f"HAS_{attr.upper()}"

        match_clauses.append(f"(b:Book)-[:{rel_type}]->({alias}:{node_label})")

        # Allow passing either a single string or a list
        if isinstance(value, list):
            params[f"{alias}_names"] = value
            where_clauses.append(f"{alias}.name IN ${alias}_names")
        else:
            params[f"{alias}_name"] = value
            where_clauses.append(f"{alias}.name = ${alias}_name")

        if not attributes:
            raise HTTPException(status_code=400, detail="At least one valid attribute required.")

    # Composing Query

    cypher = f"""
        MATCH {", ".join(match_clauses)}
        WHERE {" AND ".join(where_clauses)}
        RETURN DISTINCT b.title AS title, b.author AS author, b.year AS year, id(b) AS id
    """
    try:
        results = graph.run(cypher, **params).data()
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
