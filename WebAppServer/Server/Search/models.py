from django.db import models

class Order(models.Model):
    orderid = models.AutoField(db_column='orderID', primary_key=True)  # Field name made lowercase.
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='userid', blank=True, null=True)  # Field name made lowercase.
    carid = models.ForeignKey('Vehicle', models.DO_NOTHING, db_column='carid', blank=True, null=True)  # Field name made lowercase.
    createdate = models.CharField(db_column='createDate', max_length=10, blank=True, null=True)  # Field name made lowercase.
    pickupdate = models.CharField(db_column='pickupDate', max_length=10, blank=True, null=True)  # Field name made lowercase.
    pickupstore = models.ForeignKey('Store', models.DO_NOTHING, db_column='pickupstore', blank=True, null=True, related_name = 'store_pickup')  # Field name made lowercase.
    returndate = models.CharField(db_column='returnDate', max_length=10, blank=True, null=True)  # Field name made lowercase.
    returnstore = models.ForeignKey('Store', models.DO_NOTHING, db_column='returnstore', blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return str(self.orderid)


class Store(models.Model):
    storeid = models.AutoField(db_column='storeid', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return str(self.storeid)

class User(models.Model):
    userid = models.AutoField(db_column='userid', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=25, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    birthday = models.CharField(max_length=20, blank=True, null=True)
    occupation = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=1, blank=True, null=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    authenticationlevel = models.IntegerField(db_column='authenticationLevel', blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return str(self.userid)


class Vehicle(models.Model):
    carid = models.AutoField(db_column='carid', primary_key=True)  # Field name made lowercase.
    storeid = models.ForeignKey(Store, models.DO_NOTHING, db_column='storeid', blank=True, null=True)  # Field name made lowercase.
    carmake = models.CharField(db_column='carmake', max_length=255, blank=True, null=True)  # Field name made lowercase.
    model = models.CharField(max_length=255, blank=True, null=True)
    series = models.CharField(max_length=255, blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    enginesize = models.CharField(db_column='engineSize', max_length=20, blank=True, null=True)  # Field name made lowercase.
    fuelsystem = models.CharField(db_column='fuelSystem', max_length=255, blank=True, null=True)  # Field name made lowercase.
    tankcapacity = models.CharField(db_column='tankCapacity', max_length=60, blank=True, null=True)  # Field name made lowercase.
    carpower = models.CharField(db_column='carPower', max_length=20, blank=True, null=True)  # Field name made lowercase.
    seatingcapacity = models.IntegerField(db_column='seatingCapacity', blank=True, null=True)  # Field name made lowercase.
    standardtransmission = models.CharField(db_column='standardTransmission', max_length=20, blank=True, null=True)  # Field name made lowercase.
    carbodytype = models.CharField(db_column='carBodyType', max_length=20, blank=True, null=True)  # Field name made lowercase.
    cardrivetype = models.CharField(db_column='carDriveType', max_length=20, blank=True, null=True)  # Field name made lowercase.
    carwheelbase = models.CharField(db_column='carWheelBase', max_length=10, blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return str(self.carid)