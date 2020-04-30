# Generated by Django 3.0.4 on 2020-04-30 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_auto_20200428_1526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentphonenumber',
            name='image',
            field=models.ImageField(help_text='<h2 style="color: #008CBA;">Images size must be height: 150px and width: 300px format.</h2><br>', upload_to='service_image'),
        ),
        migrations.AlterField(
            model_name='reward',
            name='image',
            field=models.ImageField(help_text='<h2 style="color: #008CBA;">Images size must be height: 308px and width: 184px format.Can add only 4 rows.</h2><br>', upload_to='reward_images'),
        ),
        migrations.AlterField(
            model_name='slider',
            name='photo',
            field=models.ImageField(help_text='<h2 style="color: #008CBA;">Images size must be height: 1920px and width: 930px format.Can add only 3 rows.</h2>', upload_to='slider_image'),
        ),
        migrations.AlterField(
            model_name='trend',
            name='image',
            field=models.ImageField(help_text='<h2 style="color: #008CBA;">Images size must be height: 1200px and width: 809px format.Can not add more row. Can add only 4 rows.</h2>', upload_to='trend_images'),
        ),
    ]