"""
Components module - Integration layer between modules and app
"""

from typing import List, Dict, Any
from fastapi import FastAPI


def validate_routes(components: List[Dict[str, Any]]) -> bool:
    """
    Detects duplicate route paths across the provided components.
    
    Parameters:
        components (List[Dict[str, Any]]): Iterable of component metadata dictionaries; when present, each component's 'routes' key should map to an iterable of route path strings.
    
    Returns:
        True if no duplicate routes are found.
    
    Raises:
        ValueError: If a duplicate route path is detected.
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
    Register and initialize application components on the provided FastAPI app.

    This sets up the admin, forums, RTC, and alter components, collects each component's metadata, and validates their routes to detect conflicts before runtime.

    Parameters:
        app (FastAPI): The FastAPI application instance to register components and routes on.

    Raises:
        ValueError: If a route conflict is detected across components.
    """
    # Import components - following the integration chain pattern
    from components.admin_comp import setup_admin
    from components.forums_comp import setup_forums
    from components.rtc_comp import setup_rtc
    from components.alter_comp import setup_alter

    # Setup each component
    components_info = []

    # Alter component first (since it powers the alter system)
    alter_info = setup_alter(app)
    components_info.append(alter_info)

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