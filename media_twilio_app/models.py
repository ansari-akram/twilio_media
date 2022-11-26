from django.db import models


class Image(models.Model):
    image = models.ImageField()

    def __str__(self) -> str:
        return str(self.image.path)