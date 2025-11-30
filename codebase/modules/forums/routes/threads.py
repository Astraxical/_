"""
Threads routes for the forums module
"""
from fastapi import APIRouter


router = APIRouter()


@router.get("/")
def get_threads():
    """
    Get all forum threads.
    
    Returns:
        List of threads
    """
    return {"message": "List of forum threads", "data": []}


@router.get("/{thread_id}")
def get_thread(thread_id: int):
    """
    Get a specific forum thread by ID.
    
    Args:
        thread_id: ID of the thread to retrieve
    
    Returns:
        Thread information
    """
    return {"message": f"Thread {thread_id}", "data": {}}