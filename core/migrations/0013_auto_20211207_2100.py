# Generated by Django 3.2.8 on 2021-12-08 00:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_merge_20211207_2100'),
    ]

    operations = [
        migrations.DeleteModel(
            name='AgenteOferta',
        ),
        migrations.DeleteModel(
            name='AuthGroupPermissions',
        ),
        migrations.DeleteModel(
            name='AuthUserGroups',
        ),
        migrations.DeleteModel(
            name='AuthUserUserPermissions',
        ),
        migrations.DeleteModel(
            name='SolicitudPresencial',
        ),
    ]
