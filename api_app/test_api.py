import requests

response = requests.post("http://127.0.0.1:8000/books/by_attributes",
    json = {
        "attributes": {
            "Genre": "literary fiction",
            "Theme": ["alienation"],
            "NarrativeStructure": "fragmented",
            "Tone": "ironic"
        }
    }
)

print("Status:", response.status_code)
print("Response:", response.json())
