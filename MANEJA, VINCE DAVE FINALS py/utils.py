# utils.py
from datetime import datetime

def validate(location, waste, date):
    """
    Basic validation:
    - location and waste must be non-empty
    - date is optional; if provided it must match MM/DD/YYYY
    Returns True if valid.
    """
    if not location or not location.strip():
        return False
    if not waste or not waste.strip():
        return False

    if date and date.strip():
        try:
            datetime.strptime(date.strip(), "%m/%d/%Y")
        except Exception:
            return False

    return True
