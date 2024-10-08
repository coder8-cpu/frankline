# Generated by Django 4.1.9 on 2024-09-01 15:01

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='team',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=1000, null=True)),
                ('designation', models.CharField(blank=True, max_length=1000, null=True)),
                ('image', models.ImageField(upload_to='team')),
            ],
        ),
        migrations.RenameField(
            model_name='slider_text',
            old_name='text',
            new_name='data1',
        ),
        migrations.AddField(
            model_name='slider_text',
            name='data2',
            field=models.CharField(default='', max_length=1000),
            preserve_default=False,
        ),
    ]
