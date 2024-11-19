# Generated by Django 5.1.3 on 2024-11-18 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_alter_task_options_rename_create_task_created_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ['complete']},
        ),
        migrations.AddField(
            model_name='task',
            name='due_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='priority',
            field=models.CharField(choices=[('低', '低'), ('中', '中'), ('高', '高')], default='中', max_length=2),
        ),
        migrations.AlterOrderWithRespectTo(
            name='task',
            order_with_respect_to=None,
        ),
    ]
