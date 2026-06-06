from django.db import models


class Banner(models.Model):
    title      = models.CharField(max_length=300, blank=True)
    subtitle   = models.CharField(max_length=500, blank=True)
    image      = models.ImageField(upload_to='banners/')
    is_active  = models.BooleanField(default=True)
    order      = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title