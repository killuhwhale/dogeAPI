from django.db import models


class Doge(models.Model):
    id = models.IntegerField(primary_key=True)
    ts = models.DecimalField(max_digits=65535, decimal_places=65535)
    price = models.DecimalField(max_digits=65535, decimal_places=65535)

    class Meta:
        managed = False
        db_table = 'doge'
        unique_together = (('ts', 'price'),)


class Tweets(models.Model):
    id = models.IntegerField(primary_key=True)
    ts = models.DateTimeField()
    tweet = models.TextField()

    class Meta:
        managed = False
        db_table = 'tweets'
        unique_together = (('ts', 'tweet'),)
