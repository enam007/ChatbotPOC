import json
import re

def clean_html_output(raw: str) -> str:
    """Converts escaped JSON-style HTML to clean, renderable HTML safely."""
    if not raw:
        return ""

    try:
        cleaned = json.loads(raw)
    except Exception:
        cleaned = raw.encode('utf-8').decode('unicode_escape')

    cleaned = re.sub(
        r'<(script|iframe|object|embed|link|form|input|button|style[^>]*src)[^>]*?>.*?</\1>',
        '',
        cleaned,
        flags=re.IGNORECASE | re.DOTALL,
    )
    cleaned = re.sub(r'on\w+="[^"]*"', '', cleaned, flags=re.IGNORECASE)
    try:
        cleaned = cleaned.encode('latin1').decode('utf-8')
    except UnicodeEncodeError:
        pass  # already properly encoded

    return cleaned.strip()
    
