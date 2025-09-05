from django.contrib.auth.models import User
from django.db import models


class Run(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    athlete = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                related_name='athlete',
                                verbose_name='Атлет')

    class Meta:
        verbose_name = 'Пробежка'
        verbose_name_plural = 'Пробежки'
        ordering = ['-created_at']

    def __str__(self):
        return f'Пробежка {self.athlete.username} от {self.created_at}'