# Generated by Django 4.2.3 on 2023-07-24 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trainerdetails',
            name='trainer_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
