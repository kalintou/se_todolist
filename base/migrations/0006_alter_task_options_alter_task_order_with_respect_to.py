# Generated by Django 5.1.3 on 2024-11-19 03:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_alter_task_priority_alter_task_title'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='task',
            options={},
        ),
        migrations.AlterOrderWithRespectTo(
            name='task',
            order_with_respect_to='user',
        ),
    ]
