from rest_framework.views import exception_handler

def api_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is None:
        return None
    errors = response.data
    detail = errors.get("detail") if isinstance(errors, dict) else None
    response.data = {"success": False, "code": getattr(exc, "default_code", "API_ERROR").upper(), "message": str(detail or "The submitted data is invalid."), "errors": errors}
    return response
