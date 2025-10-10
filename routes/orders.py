from fastapi import APIRouter

route = APIRouter()


@route.get("/")
def get_orders():
    return {"orders": []}


@route.post("/")
def create_order():
    return {"order": {}}


@route.put("/{order_id}")
def update_order(order_id: int):
    return {"order": {"id": order_id}}


@route.delete("/{order_id}")
def delete_order(order_id: int):
    return {"order": {"id": order_id}}
