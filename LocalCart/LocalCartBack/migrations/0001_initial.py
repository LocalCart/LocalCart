# -*- coding: utf-8 -*-
# Generated by Django 1.10.dev20151020170533 on 2015-10-20 19:17
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('description', models.CharField(max_length=4096, null=True)),
                ('price', models.FloatField(max_length=4096)),
                ('picture', models.CharField(max_length=128, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('inventoryID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LocalCartBack.Inventory')),
            ],
        ),
        migrations.CreateModel(
            name='List',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('userID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ListItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=64)),
                ('list_position', models.PositiveSmallIntegerField(unique=True)),
                ('itemID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='LocalCartBack.Item')),
                ('listID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LocalCartBack.List')),
            ],
        ),
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveSmallIntegerField()),
                ('text', models.CharField(max_length=4096, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('itemID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LocalCartBack.Item')),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('address_street', models.CharField(max_length=64)),
                ('address_city', models.CharField(max_length=32)),
                ('address_state', models.CharField(max_length=32)),
                ('address_zip', models.CharField(max_length=16)),
                ('phone_number', models.CharField(max_length=16)),
                ('description', models.CharField(max_length=4096, null=True)),
                ('picture', models.CharField(max_length=128, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('userID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_type', models.CharField(max_length=16)),
                ('picture', models.CharField(max_length=128, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('userID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='reviews',
            name='storeID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LocalCartBack.Store'),
        ),
        migrations.AddField(
            model_name='reviews',
            name='userID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='item',
            name='storeID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LocalCartBack.Store'),
        ),
        migrations.AddField(
            model_name='inventory',
            name='storeID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LocalCartBack.Store'),
        ),
    ]
