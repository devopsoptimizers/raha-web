from django.db import transaction

class ModelService:
    model = None
    @classmethod
    @transaction.atomic
    def create(cls, *, actor=None, **data):
        return cls.model.objects.create(created_by=actor, updated_by=actor, **data)
    @classmethod
    @transaction.atomic
    def update(cls, instance, *, actor=None, **data):
        for field, value in data.items():
            setattr(instance, field, value)
        instance.updated_by = actor
        instance.full_clean()
        instance.save()
        return instance
