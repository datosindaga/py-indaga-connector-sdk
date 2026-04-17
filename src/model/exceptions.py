import httpx


class SdkException(Exception):
    """Base exception for all SDK errors."""

    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.status_code = status_code

    def __str__(self):
        base = super().__str__()
        return f"[HTTP {self.status_code}] {base}" if self.status_code else base


# --- 4xx Client Errors ---

class SdkBadRequestException(SdkException):
    """400 — The request was malformed or invalid."""
    def __init__(self, message: str = "Bad request"):
        super().__init__(message, status_code=400)


class SdkUnauthorizedException(SdkException):
    """401 — Missing or invalid authentication credentials."""
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(message, status_code=401)


class SdkForbiddenException(SdkException):
    """403 — Authenticated but not permitted to access this resource."""
    def __init__(self, message: str = "Forbidden"):
        super().__init__(message, status_code=403)


class SdkNotFoundException(SdkException):
    """404 — The requested resource does not exist."""
    def __init__(self, message: str = "Not found"):
        super().__init__(message, status_code=404)


class SdkConflictException(SdkException):
    """409 — The request conflicts with the current state of the resource."""
    def __init__(self, message: str = "Conflict"):
        super().__init__(message, status_code=409)


# --- 5xx Server Errors ---

class SdkServerException(SdkException):
    """5xx — An unexpected server-side error occurred."""
    def __init__(self, message: str = "Server error", status_code: int = 500):
        super().__init__(message, status_code=status_code)

def raise_for_status(response: httpx.Response) -> None:
    """Raises the appropriate SdkException for non-2xx responses."""
    if response.is_success:
        return

    message = _extract_message(response)

    match response.status_code:
        case 400: raise SdkBadRequestException(message)
        case 401: raise SdkUnauthorizedException(message)
        case 403: raise SdkForbiddenException(message)
        case 404: raise SdkNotFoundException(message)
        case 409: raise SdkConflictException(message)
        case _:   raise SdkServerException(message, status_code=response.status_code)


def _extract_message(response: httpx.Response) -> str:
    try:
        return response.json().get("message", response.text)
    except Exception:
        return response.text