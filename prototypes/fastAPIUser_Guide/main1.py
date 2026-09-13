from fastapi import FastAPI
from enum import Enum
from pydantic import BaseModel

app = FastAPI()

# Database simulation
fake_items_db = [{"item_name": "foo"}, {"item_name": "baz"}, {"item_name": "bar"}]


@app.get("/")
async def root():
    return {"message": "hola"}


@app.get("/items/{item_id}")
async def read_item(
    item_id: str, needy: str, q: str | None = None, short: bool = False
):
    """
    `item_id` = PATH PARAMETER.
    `needy`, `q`, `short` = QUERY PARAMETERS.

    /items/123?needy=juan&q=hola&short=true
    """

    item = {"item_id": item_id, "needy": needy}

    if q:
        item.update({"q": q})

    if not short:
        item.update({"description": "long ahh description"})

    return item
    """
    Dos PATH PARAMETERS:
    `user_id` e `item_id`.

    `q` y `short` son QUERY PARAMETERS.
    """


@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: str | None = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}

    if q:
        item.update({"q": q})

    if not short:
        item.update({"description": "long ahh description"})

    return item


@app.get("/items_dos/")
async def read_item_dos(skip: int = 0, limit: int = 10):
    """
    QUERY PARAMETERS porque `skip` y `limit` no están en la ruta.

    /items_dos/?skip=1&limit=2
    """
    return fake_items_db[skip : skip + limit]


class ModelName(str, Enum):
    """
    ENUM = valores válidos que puede recibir `model_name`.
    Al heredar de `str`, los valores siguen siendo strings.
    """

    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    """
    `model_name` es PATH PARAMETER,
    pero su TYPE es un ENUM.

    Solo acepta:
    alexnet, resnet, lenet
    """

    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": {"DEEP LEARNING"}}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": {"LeCNN"}}


# TESTING A FULL REQUEST BODY


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.post("/items_tres/")
async def create_item(item: Item):
    item_dict = item.model_dump()
    if item.tax is not None:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


# REQUEST BODY + PATH PARAMETERS
@app.put("/items_tres/{itemt_tres_id}")
async def update_item_query(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.model_dump()}
    if q:
        result.update({"q": q})
    return result
