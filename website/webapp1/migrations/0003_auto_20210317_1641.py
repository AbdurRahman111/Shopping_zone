# Generated by Django 3.1.4 on 2021-03-17 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp1', '0002_categories_products'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='image4',
            field=models.ImageField(blank=True, default='', null=True, upload_to='uploads/product_image'),
        ),
        migrations.AddField(
            model_name='products',
            name='image5',
            field=models.ImageField(blank=True, default='', null=True, upload_to='uploads/product_image'),
        ),
        migrations.AddField(
            model_name='products',
            name='image6',
            field=models.ImageField(blank=True, default='', null=True, upload_to='uploads/product_image'),
        ),
        migrations.AddField(
            model_name='products',
            name='image7',
            field=models.ImageField(blank=True, default='', null=True, upload_to='uploads/product_image'),
        ),
        migrations.AlterField(
            model_name='products',
            name='image',
            field=models.ImageField(default='', upload_to='uploads/product_image'),
            preserve_default=False,
        ),
    ]