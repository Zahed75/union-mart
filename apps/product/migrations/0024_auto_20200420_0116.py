# Generated by Django 3.0.4 on 2020-04-19 19:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0023_auto_20200420_0058'),
    ]

    operations = [
        migrations.RenameField(
            model_name='paymentphonenumber',
            old_name='service_name',
            new_name='payment_gateway',
        ),
    ]