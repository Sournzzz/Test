# PATH PARAMETERS, ADDING SPECIAL VALIDATION LIKE THE QUERY ONE
from typing import Annotated, Literal

from fastapi import FastAPI, Path, Query, Body
from pydantic import BaseModel, Field

app = FastAPI()


@app.get("/items/{item_id}")
async def read_items(
    # Query parameter obligatorio + validación: 0 < size < 10.5
    size: Annotated[float, Query(gt=0, lt=10.5)],
    # Path parameter obligatorio + validación: 0 < item_id <= 1000
    item_id: Annotated[int, Path(title="ID ITEM TO GET", gt=0, le=1000)],
    # Query parameter opcional + alias "item-query"
    q: Annotated[str | None, Query(alias="item-query")] = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


# Extra validation for query parameters
class FilterParams(BaseModel):
    # Rechaza query parameters que no estén definidos en el modelo
    model_config = {"extra": "forbid"}

    # Default 100 + validación: 0 < limit <= 100
    limit: int = Field(100, gt=0, le=100)

    # Default 0 + validación: offset >= 0
    offset: int = Field(0, ge=0)

    # Solo permite uno de estos dos valores
    order_by: Literal["created_at", "updated_at"] = "created_at"

    # Lista de strings
    tags: list[str] = []


@app.get("/items2/")
async def read_items2(
    # Usa FilterParams como conjunto de query parameters
    filter_query: Annotated[FilterParams, Query()],
):
    return filter_query


# Modelo para datos del body
class Item(BaseModel):
    name: str
    description: str
    price: float
    tax: float | None = None  # Campo opcional


# Otro modelo para datos del body
class User(BaseModel):
    name: str
    full_name: str | None = None  # Campo opcional


@app.put("/items/{item_id}")
async def update_item(
    # Se interpretan como datos del request body
    item: Item,
    user: User,
    # Path parameter + validación: 0 <= item_id <= 100
    item_id: Annotated[int, Path(title="ID to get the item", ge=0, le=100)],
    # Body parameter; aquí no hay validación extra
    importance: Annotated[int, Body()],
    # Query parameter opcional
    q: str | None = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results


@app.put("/items2/{item_id2}")
async def update_item2(
    # Todos los parámetros después de * deben pasarse por nombre
    *,
    # Datos del request body
    item: Item,
    user: User,
    # Path parameter + validación
    item_id: Annotated[int, Path(title="ID to get the item", ge=0, le=100)],
    # Body parameter + validación: importance > 0
    importance: Annotated[int, Body(gt=0)],
    # Query parameter opcional
    q: str | None = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results


class FilterParamsDos(BaseModel):
    # Igual: rechaza parámetros extra
    model_config = {"extra": "forbid"}

    # Default 100 + 0 < limit <= 100
    limit: int = Field(100, gt=0, le=100)

    # Default 0 + offset >= 0
    offset: int = Field(0, ge=0)

    # Solo permite estos dos valores
    order_by: Literal["created_at", "updated_at"] = "created_at"

    # Lista de strings
    tags: list[str] = []


@app.get("/items3/")
async def read_items3(
    # Usa FilterParams como query parameters
    # (ojo: aquí estás usando FilterParams, no FilterParamsDos)
    filter_query: Annotated[FilterParams, Query()],
):
    return filter_query
