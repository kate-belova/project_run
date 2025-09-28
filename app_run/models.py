from django.contrib.auth.models import User
from django.db import models


class Run(models.Model):
    STATUS_CHOICES = [
        ('init', 'Initialized'),
        ('in_progress', 'In progress'),
        ('finished', 'Finished')
    ]

    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    athlete = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                related_name='athlete',
                                verbose_name='Атлет')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,
                              default='init', verbose_name='Статус')

    class Meta:
        verbose_name = 'Пробежка'
        verbose_name_plural = 'Пробежки'
        ordering = ['-created_at']

    def __str__(self):
        return f'Пробежка {self.athlete.username} от {self.created_at}'