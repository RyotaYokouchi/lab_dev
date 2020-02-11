from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=200)
    strange_value = models.BigIntegerField(default=0)
    normal_face = models.ImageField(upload_to='images/normal_face/', blank=True, null=True)
    strange_face = models.ImageField(upload_to='images/strange_face/', blank=True, null=True)
    def __str__(self):
        return self.name
