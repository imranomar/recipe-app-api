# Generated by Django 3.2.15 on 2022-09-19 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20220915_1217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(null=True, to='core.Tag'),
        ),
    ]