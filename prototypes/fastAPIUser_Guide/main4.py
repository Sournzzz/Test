from typing import Annotated

from fastapi import Body, FastAPI
from pydantic import BaseModel, Field, HttpUrl

app = FastAPI()


class Image(BaseModel):
    url: HttpUrl
    name: str


class Item(BaseModel):
    name: str
    descritpion: str | None = Field(
        default=None, title="item description", max_length=300
    )
    price: float = Field(gt=0, description="the price must be greater than 0")
    tax: float | None = None
    tags: set[str] = set()
    images: list[Image] | None = None


class Offer(BaseModel):
    name: str
    description: str | None = None
    price: float
    items: list[Item]


@app.post("/offers/")
async def create_offer(offer: Offer):
    return offer


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Annotated[Item, Body(embed=True)]):
    results = {"item_id": item_id, "item": item}
    return results


@app.post("images/multiples")
async def create_multiple_images(images: list[Image]):
    return images
