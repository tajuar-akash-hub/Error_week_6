# Generated by Django 5.0 on 2024-02-16 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_useraddress_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userbankaccount',
            name='birth_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
