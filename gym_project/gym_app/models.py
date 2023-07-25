from django.db import models
from user_app.models import UserMaster

class FeedbackMaster(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(UserMaster, on_delete=models.CASCADE, blank=True, null=True)
    details = models.TextField(blank=True, null=True, max_length=250)
    rating = models.IntegerField()

    class Meta:
        db_table = 'feedback_master'

class PlanMaster(models.Model):
    plan_id = models.AutoField(primary_key=True)
    title = models.TextField(max_length=50)
    details = models.TextField(max_length=250)
    price = models.IntegerField()
    duration = models.TextField(max_length=20)

    class Meta:
        db_table = 'plan_master'

class MembershipMaster(models.Model):
    membership_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(UserMaster, on_delete=models.CASCADE, blank=True, null=True)
    plan_id = models.ForeignKey(PlanMaster, on_delete=models.CASCADE, blank=True, null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(auto_now=True)
    details = models.TextField(max_length=250)
    status = models.TextField(max_length=15)

    class Meta:
        db_table = 'membership_master'

class PaymentMaster(models.Model):
    payment_id = models.AutoField(primary_key=True)
    membership_id = models.ForeignKey(MembershipMaster, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.IntegerField()
    method = models.TextField(max_length=15)
    # transaction
    # receipt
    # status

    class Meta:
        db_table = 'payment_master'

class AttendanceMaster(models.Model):
    attendance_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(UserMaster, on_delete=models.CASCADE, null=True, blank=True)
    attendance_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'attendance_master'

class ProductMaster(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=50)
    quantity = models.IntegerField()
    details = models.TextField(max_length=250)
    price = models.IntegerField()

    class Meta:
        db_table = 'product_master'

class OrderMaster(models.Model):
    order_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(UserMaster, on_delete=models.CASCADE, null=True, blank=True)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_status = models.TextField(max_length=20)

    class Meta:
        db_table = 'order_master'

class OrderDetails(models.Model):
    details_id = models.AutoField(primary_key=True)
    order_id = models.ForeignKey(OrderMaster, on_delete=models.CASCADE, null=True, blank=True)
    product_id = models.ForeignKey(ProductMaster, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField()
    total_amount = models.IntegerField()

    class Meta:
        db_table = 'order_details'