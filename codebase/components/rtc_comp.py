"""
RTC Component - Integration for RTC Module
"""

from fastapi import FastAPI
from modules.rtc import router as rtc_router


def setup_rtc(app: FastAPI):
    """
    Setup the RTC module component
    """
    # Mount the RTC routes
    app.include_router(rtc_router)
    
    return {
        "name": "rtc",
        "routes": ["/rtc/*"],
        "initialized": True
    }