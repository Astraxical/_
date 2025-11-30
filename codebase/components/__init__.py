"""
Components module - Integration layer between modules and app
"""

from typing import List, Dict, Any
from fastapi import FastAPI


def validate_routes(components: List[Dict[str, Any]]) -> bool:
    """
    Validates that there are no route conflicts between components
    """
    all_routes = []
    for comp in components:
        if 'routes' in comp:
            for route in comp['routes']:
                if route in all_routes:
                    raise ValueError(f"Route conflict detected: {route}")
                all_routes.append(route)
    return True


def setup_components(app: FastAPI):
    """
    Initialize and setup all components
    """
    # Import components - following the integration chain pattern
    from components.admin_comp import setup_admin
    from components.forums_comp import setup_forums
    from components.rtc_comp import setup_rtc

    # Setup each component
    components_info = []

    # Admin component
    admin_info = setup_admin(app)
    components_info.append(admin_info)

    # Forums component
    forums_info = setup_forums(app)
    components_info.append(forums_info)

    # RTC component
    rtc_info = setup_rtc(app)
    components_info.append(rtc_info)

    # Validate all routes to prevent conflicts
    validate_routes(components_info)

    print(f"Successfully set up {len(components_info)} components")