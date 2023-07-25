# Generated by Django 4.2.3 on 2023-07-24 12:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AttendanceMaster',
            fields=[
                ('attendance_id', models.IntegerField(primary_key=True, serialize=False)),
                ('attendance_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'attendance_master',
            },
        ),
        migrations.CreateModel(
            name='FeedbackMaster',
            fields=[
                ('feedback_id', models.IntegerField(primary_key=True, serialize=False)),
                ('details', models.TextField(blank=True, max_length=250, null=True)),
                ('rating', models.IntegerField()),
            ],
            options={
                'db_table': 'feedback_master',
            },
        ),
        migrations.CreateModel(
            name='MembershipMaster',
            fields=[
                ('membership_id', models.IntegerField(primary_key=True, serialize=False)),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('end_date', models.DateTimeField(auto_now=True)),
                ('details', models.TextField(max_length=250)),
                ('status', models.TextField(max_length=15)),
            ],
            options={
                'db_table': 'membership_master',
            },
        ),
        migrations.CreateModel(
            name='OrderDetails',
            fields=[
                ('details_id', models.IntegerField(primary_key=True, serialize=False)),
                ('quantity', models.IntegerField()),
                ('total_amount', models.IntegerField()),
            ],
            options={
                'db_table': 'order_details',
            },
        ),
        migrations.CreateModel(
            name='OrderMaster',
            fields=[
                ('order_id', models.IntegerField(primary_key=True, serialize=False)),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('delivery_status', models.TextField(max_length=20)),
            ],
            options={
                'db_table': 'order_master',
            },
        ),
        migrations.CreateModel(
            name='PlanMaster',
            fields=[
                ('plan_id', models.IntegerField(primary_key=True, serialize=False)),
                ('title', models.TextField(max_length=50)),
                ('details', models.TextField(max_length=250)),
                ('price', models.IntegerField()),
                ('duration', models.TextField(max_length=20)),
            ],
            options={
                'db_table': 'plan_master',
            },
        ),
        migrations.CreateModel(
            name='ProductMaster',
            fields=[
                ('product_id', models.IntegerField(primary_key=True, serialize=False)),
                ('product_name', models.CharField(max_length=50)),
                ('quantity', models.IntegerField()),
                ('details', models.TextField(max_length=250)),
                ('price', models.IntegerField()),
            ],
            options={
                'db_table': 'product_master',
            },
        ),
        migrations.CreateModel(
            name='PaymentMaster',
            fields=[
                ('payment_id', models.IntegerField(primary_key=True, serialize=False)),
                ('amount', models.IntegerField()),
                ('method', models.TextField(max_length=15)),
                ('membership_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gym_app.membershipmaster')),
            ],
            options={
                'db_table': 'payment_master',
            },
        ),
    ]
