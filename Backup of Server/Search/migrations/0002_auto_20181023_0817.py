# Generated by Django 2.1 on 2018-10-22 22:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Search', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='test_Order',
            fields=[
                ('orderid', models.AutoField(db_column='orderID', primary_key=True, serialize=False)),
                ('createdate', models.CharField(blank=True, db_column='createDate', max_length=10, null=True)),
                ('pickupdate', models.CharField(blank=True, db_column='pickupDate', max_length=10, null=True)),
                ('returndate', models.CharField(blank=True, db_column='returnDate', max_length=10, null=True)),
            ],
            options={
                'db_table': 'test_order',
            },
        ),
        migrations.CreateModel(
            name='test_Store',
            fields=[
                ('storeid', models.AutoField(db_column='storeID', primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('city', models.CharField(blank=True, max_length=255, null=True)),
                ('state', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'test_store',
            },
        ),
        migrations.CreateModel(
            name='test_User',
            fields=[
                ('userid', models.AutoField(db_column='userID', primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('phone', models.CharField(blank=True, max_length=25, null=True)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('birthday', models.CharField(blank=True, max_length=20, null=True)),
                ('occupation', models.CharField(blank=True, max_length=255, null=True)),
                ('gender', models.CharField(blank=True, max_length=1, null=True)),
                ('username', models.CharField(blank=True, max_length=255, null=True)),
                ('password', models.CharField(blank=True, max_length=255, null=True)),
                ('authenticationlevel', models.IntegerField(blank=True, db_column='authenticationLevel', null=True)),
            ],
            options={
                'db_table': 'test_user',
            },
        ),
        migrations.CreateModel(
            name='test_Vehicle',
            fields=[
                ('carid', models.AutoField(db_column='carID', primary_key=True, serialize=False)),
                ('carmake', models.CharField(blank=True, db_column='carMake', max_length=255, null=True)),
                ('model', models.CharField(blank=True, max_length=255, null=True)),
                ('series', models.CharField(blank=True, max_length=255, null=True)),
                ('year', models.IntegerField(blank=True, null=True)),
                ('price', models.IntegerField(blank=True, null=True)),
                ('enginesize', models.CharField(blank=True, db_column='engineSize', max_length=20, null=True)),
                ('fuelsystem', models.CharField(blank=True, db_column='fuelSystem', max_length=255, null=True)),
                ('tankcapacity', models.CharField(blank=True, db_column='tankCapacity', max_length=60, null=True)),
                ('carpower', models.CharField(blank=True, db_column='carPower', max_length=20, null=True)),
                ('seatingcapacity', models.IntegerField(blank=True, db_column='seatingCapacity', null=True)),
                ('standardtransmission', models.CharField(blank=True, db_column='standardTransmission', max_length=20, null=True)),
                ('carbodytype', models.CharField(blank=True, db_column='carBodyType', max_length=20, null=True)),
                ('cardrivetype', models.CharField(blank=True, db_column='carDriveType', max_length=20, null=True)),
                ('carwheelbase', models.CharField(blank=True, db_column='carWheelBase', max_length=10, null=True)),
                ('storeid', models.ForeignKey(blank=True, db_column='storeID', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='Search.test_Store')),
            ],
            options={
                'db_table': 'test_vehicle',
            },
        ),
        migrations.AddField(
            model_name='test_order',
            name='carid',
            field=models.ForeignKey(blank=True, db_column='carID', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='Search.test_Vehicle'),
        ),
        migrations.AddField(
            model_name='test_order',
            name='pickupstore',
            field=models.ForeignKey(blank=True, db_column='pickupStore', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='test_store_pickup', to='Search.test_Store'),
        ),
        migrations.AddField(
            model_name='test_order',
            name='returnstore',
            field=models.ForeignKey(blank=True, db_column='returnStore', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='Search.test_Store'),
        ),
        migrations.AddField(
            model_name='test_order',
            name='userid',
            field=models.ForeignKey(blank=True, db_column='userID', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='Search.test_User'),
        ),
    ]