# Generated by Django 3.2.3 on 2021-05-16 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_alter_cartproducts_productimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='AllCategories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CategoryName', models.CharField(max_length=200)),
                ('CategoryImage', models.ImageField(upload_to='categorymedia')),
            ],
        ),
        migrations.CreateModel(
            name='AllProducts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ProductName', models.CharField(max_length=200)),
                ('ProductPrice', models.IntegerField()),
                ('ProductImage', models.ImageField(upload_to='productsmedia')),
            ],
        ),
    ]
