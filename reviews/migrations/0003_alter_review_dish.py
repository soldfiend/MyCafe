# Generated by Django 4.2.5 on 2023-09-16 18:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
        ('reviews', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='dish',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='menu.dish'),
        ),
    ]
