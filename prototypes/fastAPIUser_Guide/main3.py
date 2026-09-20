#PATH PARAMETERS, ADDING SPECIAL VALIDATION LIKE THE QUERY ONE 
from typing import Annotated 

from fastapi import FastAPI, Path, Query

app = FastAPI()
@app.get("/items/{item_id}")
async def read_items(
    item_id: Annotated[int, Path(title="ID ITEM TO GET", gt=0, le=1000)],
    q: Annotated[str | None, Query(alias="item-query")] = None,
    size: Annotated[float, Query(gt=0, lt=10.5)],
):
    results = {"item_id" : item_id}
    if q: 
        results.update({"q":q})
    return results


