import time
from .models import AuditLog

class AuditLogMiddleware:
    def __init__(self,get_response): self.get_response=get_response
    def __call__(self,request):
        started_at=time.monotonic()
        response=self.get_response(request)
        if request.path.startswith("/api/"):
            forwarded=request.META.get("HTTP_X_FORWARDED_FOR","").split(",")[0].strip()
            try:
                AuditLog.objects.create(
                    actor=request.user if getattr(request,"user",None) and request.user.is_authenticated else None,
                    method=request.method,
                    path=request.get_full_path()[:500],
                    status_code=response.status_code,
                    ip_address=forwarded or request.META.get("REMOTE_ADDR"),
                    user_agent=request.META.get("HTTP_USER_AGENT","")[:500],
                    metadata={"duration_ms":round((time.monotonic()-started_at)*1000,2)},
                )
            except Exception:
                # Audit persistence must never turn a successful API response into a failure.
                pass
        return response
