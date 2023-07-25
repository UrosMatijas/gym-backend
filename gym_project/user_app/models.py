from django.db import models
from django.contrib.auth.models import User

class UserType(models.Model):
    type_id = models.IntegerField(primary_key=True)
    user_type = models.CharField(unique=True, max_length=10, blank=True, null=True)

    class Meta:
        db_table = 'user_type'

    def __str__(self):
        return self.user_type

class UserMaster(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    type = models.ForeignKey('UserType', on_delete=models.CASCADE, blank=True, null=True)
    user_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=17)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    mobile = models.CharField(max_length=30)

    class Meta:
        db_table = 'user_master'

    def __str__(self):
        return self.user_name

class TrainerDetails(models.Model):
    trainer_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey('UserMaster', on_delete=models.CASCADE)
    salary = models.IntegerField()
    details = models.TextField(max_length=250)

    class Meta:
        db_table = 'trainer_details'







