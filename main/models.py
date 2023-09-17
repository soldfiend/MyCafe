from django.db import models


class HomePagePhoto(models.Model):
    image = models.ImageField(upload_to='home_page_photos/')
    caption = models.CharField(max_length=255)

    def __str__(self):
        return self.caption
