from fastapi import FastAPI
from enum import Enum


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


app = FastAPI()

fake_items_db = [{"item_name": "foo"}, {"item_name": "baz"}, {"item_name": "bar"}]


@app.get("/items_dos/")
async def read_item_dos(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]


@app.get("/")
async def root():
    return {"message": "hola"}


@app.get("/items/{item_id}")
async def read_item(
    item_id: str, needy: str, q: str | None = None, short: bool = False
):
    item = {"item_id": item_id, "needy": needy}
    if q:
        item.update({"q": q})
    if not short:
        item.update({"description": "long ahh description"})
    return item


@app.get("users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: str | None = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update({"description": "long ahh description"})
    return item


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": {"DEEP LEARNING"}}
    if model_name.value == "lenet":
        return {"model_name": model_name, "message": {"LeCNN"}}
