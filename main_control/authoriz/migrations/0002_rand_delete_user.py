# Generated by Django 4.2 on 2023-04-14 01:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_apis', '0002_alter_heartbeat_user_name'),
        ('authoriz', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
            ],
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]