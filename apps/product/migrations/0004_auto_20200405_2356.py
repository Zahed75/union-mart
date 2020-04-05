# Generated by Django 3.0.4 on 2020-04-05 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_auto_20200403_2323'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'Product', 'verbose_name_plural': 'Products'},
        ),
        migrations.AlterModelOptions(
            name='productphoto',
            options={'verbose_name': 'Product Photo', 'verbose_name_plural': 'Product Photos'},
        ),
        migrations.RemoveField(
            model_name='product',
            name='photo',
        ),
        migrations.AddField(
            model_name='product',
            name='default_photo',
            field=models.ImageField(default=1, help_text='Product default image.', upload_to='product_image'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Product Name'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.PositiveIntegerField(verbose_name='Product Price'),
        ),
        migrations.AlterField(
            model_name='product',
            name='stock',
            field=models.PositiveIntegerField(verbose_name='Stock of Products'),
        ),
        migrations.AlterField(
            model_name='product',
            name='type',
            field=models.CharField(max_length=20, verbose_name='Product Type'),
        ),
        migrations.AlterField(
            model_name='productphoto',
            name='image',
            field=models.ImageField(upload_to='product-images'),
        ),
    ]
