from django.db import models

class Kandidat(models.Model):
    fio = models.CharField(max_length=255)


class Document(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField(blank=True, null=True)
    kandidat = models.ForeignKey(Kandidat, on_delete=models.CASCADE)

