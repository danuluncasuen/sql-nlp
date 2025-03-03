import spacy
from spacy.pipeline import EntityRuler

nlp = spacy.load("en_core_web_sm")
text = "Show me all user where age is greater than 25"

doc = nlp(text)

for token in doc:
    print(f"{token.text} -> {token.dep_} -> {token.head.text}")


ruler = nlp.add_pipe("entity_ruler", before="ner")
patterns = [
    {"label": "TABLE", "pattern": "users"},
    {"label": "COLUMN", "pattern": "age"},
    {"label": "COLUMN", "pattern": "name"},
    {"label": "VALUE", "pattern": "25"},
    {"label": "CONDITION", "pattern": "greater than"}
]
ruler.add_patterns(patterns)

doc = nlp("Get all users where age is greater than 25")

for ent in doc.ents:
    print(f"{ent.text} - {ent.label_}")


def generate_sql(doc):
    table = None
    column = None
    value = None
    condition = None

    for ent in doc.ents:
        if ent.label_ == "TABLE":
            table = ent.text
        elif ent.label_ == "COLUMN":
            column = ent.text
        elif ent.label_ == "VALUE":
            value = ent.text
        elif ent.label_ == "CONDITION":
            if ent.text == "greater than":
                condition = ">"
            elif ent.text == "less than":
                condition = "<"

    if table and column and value and condition:
        return f"SELECT * FROM {table} WHERE {column} {condition} {value};"
    return None

query = "Get all users where age is greater than 25"
doc = nlp(query)
sql = generate_sql(doc)
print(sql)