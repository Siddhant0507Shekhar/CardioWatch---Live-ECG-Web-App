# Generated by Django 4.2 on 2023-04-14 01:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authoriz', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Heartbeat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('beat', models.IntegerField()),
                ('date', models.DateTimeField()),
                ('user_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authoriz.user')),
            ],
        ),
    ]
