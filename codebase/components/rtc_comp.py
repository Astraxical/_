"""
RTC Component - Integration for RTC Module
"""

from fastapi import FastAPI
from modules.rtc import router as rtc_router


def setup_rtc(app: FastAPI):
    """
    Register the RTC router on the given FastAPI application and return component metadata.
    
    Returns:
        dict: Metadata for the RTC component with keys:
            - "name": "rtc"
            - "routes": list of mounted route patterns (e.g., ["/rtc/*"])
            - "initialized": `True` when the routes have been included
    """
    # Mount the RTC routes
    app.include_router(rtc_router)
    
    return {
        "name": "rtc",
        "routes": ["/rtc/*"],
        "initialized": True
    }