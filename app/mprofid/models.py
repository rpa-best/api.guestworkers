from django.db import models


class WorkerInvoice(models.Model):
    id = models.BigIntegerField(primary_key=True)
    worker = models.ForeignKey('oauth.User', models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
