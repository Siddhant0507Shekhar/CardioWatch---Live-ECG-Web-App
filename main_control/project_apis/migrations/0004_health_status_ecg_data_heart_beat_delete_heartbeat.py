# Generated by Django 4.2 on 2023-04-17 00:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('project_apis', '0003_ecg_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='Health_Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('health', models.IntegerField()),
                ('date', models.DateField()),
                ('timer', models.TimeField()),
                ('user_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='ecg_data',
            name='heart_beat',
            field=models.IntegerField(default=70),
        ),
        migrations.DeleteModel(
            name='Heartbeat',
        ),
    ]