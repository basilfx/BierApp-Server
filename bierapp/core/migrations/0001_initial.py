# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('value', models.DecimalField(max_digits=10, decimal_places=2)),
                ('is_app_visible', models.BooleanField(default=True)),
                ('logo', models.ImageField(height_field=b'logo_height', width_field=b'logo_width', null=True, upload_to=b'apps/bierapp/logos/')),
                ('logo_height', models.PositiveIntegerField(null=True)),
                ('logo_width', models.PositiveIntegerField(null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProductGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('is_app_visible', models.BooleanField(default=True)),
                ('site', models.ForeignKey(related_name='product_groups', to='accounts.Site')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(default=None, max_length=255, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('site', models.ForeignKey(related_name='transactions', to='accounts.Site')),
            ],
            options={
                'ordering': ('-created',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TransactionItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('count', models.IntegerField(default=0)),
                ('value', models.DecimalField(max_digits=10, decimal_places=2)),
                ('accounted_user', models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL)),
                ('executing_user', models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(to='core.Product')),
                ('product_group', models.ForeignKey(to='core.ProductGroup')),
                ('transaction', models.ForeignKey(related_name='transaction_items', to='core.Transaction')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TransactionTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TransactionTemplateCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('site', models.ForeignKey(related_name='+', to='accounts.Site')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TransactionTemplateItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('count', models.IntegerField(default=0)),
                ('product', models.ForeignKey(to='core.Product')),
                ('transaction_template', models.ForeignKey(related_name='items', to='core.TransactionTemplate')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='XPTransaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.IntegerField()),
                ('description', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('parent', models.ForeignKey(to='core.XPTransaction', null=True)),
                ('site', models.ForeignKey(related_name='xp_transactions', to='accounts.Site')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='transactiontemplate',
            name='category',
            field=models.ForeignKey(related_name='+', to='core.TransactionTemplateCategory'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='product_group',
            field=models.ForeignKey(related_name='products', to='core.ProductGroup'),
            preserve_default=True,
        ),
    ]
