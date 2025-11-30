"""
WebSocket routes for the RTC module
"""
from fastapi import APIRouter


router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(websocket):
    """
    WebSocket endpoint for real-time communication.
    
    Args:
        websocket: WebSocket connection
    """
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Echo: {data}")
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        await websocket.close()


@router.get("/")
def get_rtc_info():
    """
    Get information about the RTC module.
    
    Returns:
        Information about the RTC module
    """
    return {"message": "RTC module is running", "features": ["websockets", "real-time messaging"]}