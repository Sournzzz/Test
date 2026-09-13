from fastapi import FastAPI
from fastapi import Query
from typing import Annotated

app = FastAPI()


# ADDING EXTRA VALIDATION WITH QUERY, ANNOTATED AND REGEX
@app.get("/items/")
async def read_items(
    q: Annotated[
        str | None, Query(min_length=3, max_length=50, pattern="^fixedquery$")
    ] = None,  # <- WHEN YOU WANT TE QUERY TO BE REQUIRED YOU JUST AVOID DECLARING A PREDETERMINED PARAMETER
):
    results = {"items": [{"item_id": "foo"}, {"item_id": "bar"}]}
    if q:
        results.update({"q": q})
    return results


# MORE ANNOTATIONS
@app.get("/items2/")
async def read_items2(q: Annotated[list[str] | None, Query()] = ["Foo", "Bar"]):
    query_items = {"q": q}
    return query_items


# http:/localhost:8000/items2/?q=foo&q=bar


# ADDING MORE METADATA FOR THE CONFIGURATION OF SWAGGER
@app.get("/items3/")
async def read_items3(
    q: Annotated[
        list[str] | None,
        Query(
            min_length=5,
            max_length=50,
            title="Query string",
            description="Query string for the items to search in the db that have a good match",
        ),
    ] = None,
):
    query_items = {"q": q}
    return query_items


# ADDING MORE METADATA FOR THE CONFIGURATION OF DOCS
@app.get("/items3/")
async def read_items3(
    q: Annotated[
        list[str] | None,
        Query(
            min_length=5,
            max_length=50,
            title="Query string",
            description="Query string for the items to search in the db that have a good match",
            deprecated=True,  # ADDED THIS SO THE DOCUMENTATION SHOWS IT
            include_in_schema=False,  # HIDDEN FROM THE OpenAPI schema
        ),
    ] = None,
):
    query_items = {"q": q}
    return query_items


data = {
    "isbn-9781529046137": "The Hitchhiker's Guide to the Galaxy",
    "imdb-tt0371724": "The Hitchhiker's Guide to the Galaxy",
    "isbn-9781439512982": "Isaac Asimov: The Complete Stories, Vol. 2",
}


def check_valid_id(id: str):
    if not id.startswith(("isbn-", "imdb-")):
        raise ValueError('Invalid ID format, it must start with "isbn-" or "imdb-"')
    return id


@app.get("/items4/")
async def read_items4(
    id: Annotated[str | None, AfterValidator(check_valid_id)] = None,
):
    if id:
        item = data.get(id)
    else:
        id, item = random.choice(list(data.items()))
    return {"id": id, "name": item}
