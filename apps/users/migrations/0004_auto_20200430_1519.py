# Generated by Django 3.0.4 on 2020-04-30 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_remove_user_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_name',
            field=models.CharField(blank=True, help_text='User name can only contain letters, numbers and hyphen.', max_length=20, unique=True, verbose_name='user name'),
        ),
    ]
