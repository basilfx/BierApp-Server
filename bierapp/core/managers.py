from django.db import models


class ApiManager(models.Manager):
    def __init__(self, field="is_app_visible", *args, **kwargs):
        super(ApiManager, self).__init__(*args, **kwargs)

        # Precompute filter
        self.object_filter = {
            field: True
        }

    def get_queryset(self):
        return super(ApiManager, self).get_queryset().filter(**self.object_filter)
