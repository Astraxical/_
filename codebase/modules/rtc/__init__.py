"""
RTC Module - Real-Time Communication
"""
from fastapi import APIRouter


# Export the router for component integration
router = APIRouter(prefix="/rtc")


def get_module_info():
    """Return module-specific information for registry"""
    return {
        "name": "rtc",
        "routes": ["/rtc/*"],
        "local_data_path": "modules/rtc/data"
    }