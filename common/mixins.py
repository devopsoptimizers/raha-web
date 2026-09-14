class AuditActorMixin:
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user if self.request.user.is_authenticated else None, updated_by=self.request.user if self.request.user.is_authenticated else None)
    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user if self.request.user.is_authenticated else None)
