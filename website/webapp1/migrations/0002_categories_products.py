# Generated by Django 3.1.4 on 2021-03-17 09:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp1', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='products',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=2000)),
                ('product_price', models.CharField(max_length=2000)),
                ('image', models.ImageField(blank=True, default='', null=True, upload_to='uploads/product_image')),
                ('image2', models.ImageField(blank=True, default='', null=True, upload_to='uploads/product_image')),
                ('image3', models.ImageField(blank=True, default='', null=True, upload_to='uploads/product_image')),
                ('description', models.TextField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp1.categories')),
            ],
        ),
    ]
