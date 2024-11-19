from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('低', '低'),
        ('中', '中'),
        ('高', '高'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True)
    priority = models.CharField(max_length=2, choices=PRIORITY_CHOICES, default='中')
    order = models.PositiveIntegerField(default=0, blank=False, null=False)  # 新增字段

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order']  # 默认按 'order' 字段排序