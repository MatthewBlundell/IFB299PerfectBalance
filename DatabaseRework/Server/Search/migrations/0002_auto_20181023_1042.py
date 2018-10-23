# Generated by Django 2.1 on 2018-10-23 00:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Search', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='carid',
        ),
        migrations.RemoveField(
            model_name='order',
            name='pickupstore',
        ),
        migrations.RemoveField(
            model_name='order',
            name='returnstore',
        ),
        migrations.RemoveField(
            model_name='order',
            name='userid',
        ),
        migrations.RemoveField(
            model_name='vehicle',
            name='storeid',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.DeleteModel(
            name='Store',
        ),
        migrations.DeleteModel(
            name='User',
        ),
        migrations.DeleteModel(
            name='Vehicle',
        ),
    ]
