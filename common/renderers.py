from rest_framework.renderers import JSONRenderer

class StandardJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = (renderer_context or {}).get("response")
        if response is None or getattr(response, "exception", False):
            return super().render(data, accepted_media_type, renderer_context)
        if isinstance(data, dict) and "success" in data:
            payload = data
        elif isinstance(data, dict) and "data" in data and "meta" in data:
            payload = {"success": True, "code": "LIST_FOUND", "message": "Records retrieved successfully.", **data}
        else:
            payload = {"success": True, "code": "REQUEST_SUCCESS", "message": "Request completed successfully.", "data": data}
        return super().render(payload, accepted_media_type, renderer_context)
