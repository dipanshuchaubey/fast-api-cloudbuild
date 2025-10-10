from fastapi import APIRouter

route = APIRouter()


@route.get("/")
def get_inventory():
    return {"inventory": []}


@route.post("/")
def create_inventory():
    return {"inventory": {}}


@route.put("/{inventory_id}")
def update_inventory(inventory_id: int):
    return {"inventory": {"id": inventory_id}}


@route.delete("/{inventory_id}")
def delete_inventory(inventory_id: int):
    return {"inventory": {"id": inventory_id}}
