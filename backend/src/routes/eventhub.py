from fastapi import APIRouter
from services import send_event

router = APIRouter()


@router.post("/output")
async def send_eventhub_message(payload: dict):
    #
    # Example Event Message function...
    #
    result = await send_event(payload)
    return {"status": "sent", "result": result}

