# Generated by Django 4.1.4 on 2023-06-09 16:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basic_auth', '0002_alter_people_options'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='people',
            unique_together={('id', 'email')},
        ),
    ]