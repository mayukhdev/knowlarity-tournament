# Generated by Django 2.2 on 2019-04-14 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0002_auto_20190414_0818'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sport',
            name='name',
            field=models.CharField(choices=[('TT', 'Table Tennis'), ('FB', 'Foos Ball')], default='TT', max_length=2),
        ),
    ]