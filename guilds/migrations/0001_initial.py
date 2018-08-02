# Generated by Django 2.0.7 on 2018-08-02 20:49

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('characters', '0003_character_wallet'),
    ]

    operations = [
        migrations.CreateModel(
            name='Guild',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('is_public', models.BooleanField(default=True)),
                ('public_url', models.CharField(default=uuid.uuid4, max_length=255, unique=True)),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='characters.Character')),
                ('members', models.ManyToManyField(related_name='members', to='characters.Character')),
            ],
        ),
    ]
