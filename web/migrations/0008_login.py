# Generated by Django 4.1.9 on 2024-09-10 00:29

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0007_remove_assets_difference_amount_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='LOGIN',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('mobile_no', models.CharField(blank=True, max_length=1000, null=True)),
            ],
        ),
    ]
