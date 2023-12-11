# Generated by Django 5.0 on 2023-12-11 17:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AstronomyShow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
            ],
            options={
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='PlanetariumDome',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('rows', models.IntegerField()),
                ('seats_in_row', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ShowSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('show_time', models.DateTimeField()),
                ('astronomy_show', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='show_sessions', to='planetarium.astronomyshow')),
                ('planetarium_dome', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='show_sessions', to='planetarium.planetariumdome')),
            ],
            options={
                'ordering': ['show_time'],
            },
        ),
        migrations.CreateModel(
            name='ShowTheme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('astronomy_show', models.ManyToManyField(related_name='show_themes', to='planetarium.astronomyshow')),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('row', models.IntegerField()),
                ('seat', models.IntegerField()),
                ('reservation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='planetarium.reservation')),
                ('show_session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='planetarium.showsession')),
            ],
        ),
    ]
