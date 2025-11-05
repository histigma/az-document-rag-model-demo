__all__ = (
    'send_event',
)

async def send_event(payload: dict):
    print("Sending event:", payload)
    return {"success": True}

