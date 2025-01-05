from rest_framework.renderers import JSONRenderer

class CustomJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response_data = {
            "status": "success" if renderer_context["response"].status_code < 400 else "error",
            "message": renderer_context.get("response").status_text,
            "data": data if renderer_context["response"].status_code < 400 else None,
            "errors": data if renderer_context["response"].status_code >= 400 else None,
        }
        return super().render(response_data, accepted_media_type, renderer_context)
