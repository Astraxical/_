"""
RTC Module - Real-Time Communication
"""
from fastapi import APIRouter
from .routes import chat


# Export the router for component integration
router = APIRouter(prefix="/rtc")
router.include_router(chat.router)


def get_module_info():
    """
    Provide metadata for the RTC module used by external registries.

    Returns:
        module_info (dict): Dictionary with module metadata:
            - name (str): Module identifier ("rtc").
            - routes (list[str]): Route patterns exposed by the module (e.g., "/rtc/*").
            - local_data_path (str): Relative path to the module's local data directory ("modules/rtc/data").
    """